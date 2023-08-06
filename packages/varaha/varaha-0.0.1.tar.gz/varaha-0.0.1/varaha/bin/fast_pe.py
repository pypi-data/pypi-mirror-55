#! /usr/bin/env python

# Copyright (C) 2019  Charlie Hoy <charlie.hoy@ligo.org>
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import json
import shutil
import os
import re
import ast
import stat
import argparse
from glob import glob
import configparser


frame_types = {
    "H1": "H1_HOFT_C00",
    "L1": "L1_HOFT_C00",
    "V1": "V1Online"
}


parameter_name_conversion = {
    "mchirp": "chirp_mass",
    "tcs_refdet": "geocent_time",
    "cosi": "cos_iota",
    "iota": "iota",
    "q": "mass_ratio",
    "spin2z": "a_2",
    "spin1z": "a_1",
    "ra": "ra",
    "dPsi": "psi",
    "lumd": "luminosity_distance",
    "dec": "dec",
    "likelihood": "likelihood",
    "log_likelihood": "log_likelihood",
    "phic": "phase",
    "lkl_extr": "extrinsic_likelihood",
    "weights": "weights",
    "probability": "probability"
}


class ConfigAction(argparse.Action):
    """Class to extend the argparse.Action to handle dictionaries as input
    """
    def __init__(self, option_strings, dest, nargs=None, const=None,
                 default=None, type=None, choices=None, required=False,
                 help=None, metavar=None):
        super(ConfigAction, self).__init__(
            option_strings=option_strings, dest=dest, nargs=nargs,
            const=const, default=default, type=str, choices=choices,
            required=required, help=help, metavar=metavar)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)

        items = {}
        config = configparser.ConfigParser()
        try:
            config.read(values)
            sections = config.sections()
            for section in sections:
                for key, value in config.items(section):
                    if value == "True" or value == "true":
                        items[key] = True
                    elif value == "None" or value == "none":
                        items[key] = None
                    else:
                        if ":" in value or "{" in value:
                            items[key] = self.dict_from_str(value)
                        elif "," in value:
                            items[key] = self.list_from_str(value)
                        else:
                            items[key] = value
        except Exception:
            pass
        for i in vars(namespace).keys():
            if i in items.keys():
                setattr(namespace, i, items[i])

    def dict_from_str(self, string):
        """Reformat the string into a dictionary

        Parameters
        ----------
        string: str
            string that you would like reformatted into a dictionary
        """
        string = string.replace("'", "")
        string = string.replace('"', '')
        string = string.replace("=", ":")
        string = string.replace(" ", "")
        string = re.sub(r'([A-Za-z/\.0-9][^\[\],:"}]*)', r'"\g<1>"', string)
        string = string.replace('""', '"')
        try:
            mydict = ast.literal_eval(string)
        except ValueError as e:
            pass
        for key in mydict:
            if isinstance(mydict[key], str) and mydict[key].lower() == "true":
                mydict[key] = True
            elif isinstance(mydict[key], str) and mydict[key].lower() == "false":
                mydict[key] = False
            else:
                try:
                    mydict[key] = int(mydict[key])
                except ValueError:
                    try:
                        mydict[key] = float(mydict[key])
                    except ValueError:
                        mydict[key] = mydict[key]
        return mydict

    @staticmethod
    def list_from_str(string):
        """Reformat the string into a list

        Parameters
        ----------
        string: str
            string that you would like reformatted into a list
        """
        list = []
        if "[" in string:
            string.replace("[", "")
        if "]" in string:
            string.replace("]", "")
        if ", " in string:
            list = string.split(", ")
        elif " " in string:
            list = string.split(" ")
        elif "," in string:
            list = string.split(",")
        return list


def command_line():
    """Generate an Argument Parser object to control the command line options

    Returns
    -------
    parser: argparse.ArgumentParser
        argparse object containing possible command line options
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
       "varaha", nargs='?', help=(
           "configuration file containing the command line arguments"
       ), action=ConfigAction
    )
    analysis_group = parser.add_argument_group(
        "Options to specify the sampler settings"
    )
    analysis_group.add_argument("--gid", help="GID of the event you wish to analyse")
    analysis_group.add_argument(
        "--nparallel", help="The number of of CPUs to use for the analysis",
        default=18
    )
    analysis_group.add_argument(
        "--chunks", help="The number of chunks to split the waveform up into",
        default=1
    )
    analysis_group.add_argument(
        "--dt", help=(
            "Time window around the provided GPS within which the signal is coalescing"
        ), default=1.
    )
    analysis_group.add_argument(
        "--neff", help="The number of effective samples you wish to collect",
        default=1000
    )
    analysis_group.add_argument(
        "--burnin", help="The number of samples to discard as burnin",
        default=20000
    )
    path_group = parser.add_argument_group(
        "Options to specify where to save the output from varaha"
    )
    path_group.add_argument(
        "--outdir", help="Directory to store the output of the code", default=None
    )
    path_group.add_argument(
        "--webdir", help="Directory to store the summary pages", default=None
    )
    data_group = parser.add_argument_group(
        "Options specific to gravitational wave data collection"
    )
    data_group.add_argument(
        "--grab_data", help=(
            "Only query gw_data_find and return gravitational wave strain data"
        ), action="store_true", default=False
    )
    data_group.add_argument(
        "--types", help="Type of frame to look for with gw_data_find",
        default=frame_types
    )
    data_group.add_argument(
        "--channels", help="Channels to use to read h(t) frame files",
        default=None
    )
    data_group.add_argument(
        "--glob_frame_data", help=(
            "Directory to search for saved gravitational wave frame data"
        ), default=None
    )
    psd_group = parser.add_argument_group("Options specific for PSDs")
    psd_group.add_argument(
        "--h1_psd", help="PSD to use for the LIGO Hanford detector", default=None
    )
    psd_group.add_argument(
        "--l1_psd", help="PSD to use for the LIGO Livingston detector", default=None
    )
    psd_group.add_argument(
        "--v1_psd", help="PSD to use for the Virgo detector", default=None
    )
    psd_group.add_argument(
        "--glob_gracedb_psd", help="Directory to search for a saved psd.xml.gz file",
        default=None
    )
    trigger_group = parser.add_argument_group(
        "Options specific to the gravitational wave trigger"
    )
    trigger_group.add_argument(
        "--coinc", help="coinc.xml file to use in the analysis", default=None
    )
    condor_group = parser.add_argument_group(
        "Options specific to the HT Condor schedular"
    )
    condor_group.add_argument(
        "--condor", help="Setup a condor dag for the job", default=False,
        action="store_true"
    )
    condor_group.add_argument(
        "--condor_submit", help="Setup and submit a condor dag for the job",
        default=False, action="store_true"
    )
    condor_group.add_argument(
        "--accounting_group", help="The accounting group to use",
        default="aluk.dev.o2.cbc.explore.test"
    )
    condor_group.add_argument(
        "--accounting_group_user", help="The accounting group user",
        default=None
    )
    return parser


def get_executable(executable):
    """Find the path to the executable

    Parameters
    ----------
    executable: str
        the name of the executable you wish to find
    """
    from distutils.spawn import find_executable

    return find_executable(executable)


def main_job_imports():
    """Import the relevant packages for the main job
    """
    global sys
    import sys
    global pe
    from varaha import parameter_estimation as pe
    global np
    import numpy as np
    global TimeSeries
    from gwpy.timeseries import TimeSeries


def reweight_equal(full_pe, weights):
    """Reweight the posterior samples

    Parameters
    ----------
    full_pe: dict
        dictionary of posterior_samples
    weights: list
        list of weights for each sample

    Returns
    -------
    full_pe: dict
        reweighted dictionary of posterior_samples
    """
    parameters = full_pe.keys()

    if abs(np.sum(weights) - 1.) > 0.:
        weights = np.array(weights) / np.sum(weights)

    nsamples = len(weights)
    positions = (np.random.random() + np.arange(nsamples)) / nsamples
    idx = np.zeros(nsamples, dtype=np.int)
    cumulative_sum = np.cumsum(weights)
    i, j = 0, 0
    while i < nsamples:
        if positions[i] < cumulative_sum[j]:
            idx[i] = j
            i += 1
        else:
            j += 1
    return {i: full_pe[i][idx] for i in parameters}


def respond_to_lvalert(FarThr, alert):
    """Respond to an lvalert

    Parameters
    ----------
    FarThr: float
        The False Alarm Rate threhold to start PE
    alert: dict
        The information from the lvalert

    Returns
    -------
    template_params: dict
        dictionary containing the best matching template
    """
    cond1 = alert["alert_type"] == "new"
    cond2 = alert["object"]["far"] < FarThr
    cond3 = alert['data']['group'] == 'CBC'
    cond4 = alert['object']['search'] != 'MDC'

    if cond1 and cond2 and cond3 and con4:
        template_params = {
            "gps_time": alert["data"]["gpstime"],
            "ifo": [],
            "channel": []
        }
        for i in alert["data"]["extra_attributes"]["SingleInspiral"]:
            template_params["ifo"].append(i["ifo"])
            template_params["channel"].append(i["channel"])
            template_params["mass_1"] = i["mass1"]
            template_params["mass_2"] = i["mass2"]
            template_params["spin_1z"] = i["spin1z"]
            template_params["spin_2z"] = i["spin2z"]
    else:
        template_params = {}
    return template_params


def get_gps_start_and_stop(template_params, maxsegl):
    """Return the gps start and and end times that will encompass the best matching
    template

    Parameters
    ----------
    template_params: dict
        dictionary of the best matching template parameters
    maxself: float
        maximum segment length

    Returns
    -------
    times: list
        list containing the gps start and gps end times
    """
    from pycbc.waveform import get_td_waveform

    hp, hc = get_td_waveform(
        approximant="IMRPhenomD",
        mass1=template_params["mass_1"],
        mass2=template_params["mass_2"],
        spin1z=template_params["spin_1z"],
        spin2z=template_params["spin_2z"],
        f_lower=20.,
        delta_t=1./4096
    )
    duration = hp.duration
    if duration < 8.:
        duration = 8.
    gps_start = template_params["gps_time"] - maxsegl * 0.75
    gps_end = template_params["gps_time"] + maxsegl * 0.25
    return gps_start, gps_end
    

def gwpy_timeseries(channel, gps_start, gps_stop, frametype):
    """Return a gwpy timeseries object

    Parameters
    ----------
    channel: str
    gps_start: float
    gps_end: float
    frame_type: str
    """
    timeseries = TimeSeries.get(
        channel, gps_start, gps_stop, frametype=frametype
    )
    return timeseries.astype(np.float64)


def get_time_domain_strain(template_params, maxsegl):
    """Return the time domain strain for the given gps time

    Parameters
    ----------
    template_params: dict
        dictionary of the best matching template parameters
    maxsegl: float
        maximum segment length

    Returns
    -------
    strain: dict
        dictionary containing the time series for each detector
    """
    ts = {}
    gps_start, gps_stop = get_gps_start_and_stop(template_params, maxsegl)
    for ifo, channel in zip(template_params["ifo"], template_params["channel"]):
        timeseries = gwpy_timeseries(
            '{}:{}'.format(ifo, channel), gps_start, gps_stop, frame_types[ifo]
        )
        ts[ifo] = timeseries.to_pycbc()
    return ts


def write_frequency_domain_strain(template_params, outdir, maxsegl):
    """Write the frequency domain strain for the given gps time to file

    Parameters
    ----------
    template_params: dict
        dictionary of the best matching template parameters
    outdir: str
        The directory to store the downloaded data
    """
    from pycbc import frame

    timeseries = get_time_domain_strain(template_params, maxsegl)
    fs = {}
    for num, ifo in enumerate(timeseries.keys()):
        timeseries[ifo].to_frequencyseries().save(
            "{}/{}_frequencyseries.hdf".format(outdir, ifo),
            ifo=ifo
        )


def read_frequency_domain_strain(outdir, frame_files={}):
    """Read a frequency domain strain gwf file

    Parameters
    ----------
    outdir: str
        The directory to store the downloaded data
    frame_files: dict
        dictionary of frame files to use

    Returns
    -------
    fs: dict
        dictionary of frequency domain strains
    """
    from pycbc.types.frequencyseries import load_frequencyseries

    if frame_files == {}:
        files = glob("{}/*_frequencyseries.hdf".format(outdir))
        ifos = [i.split("/")[-1].split("_frequencyseries.hdf")[0] for i in files]
        frame_files = {ifo: f for ifo, f in zip(ifos, files)}

    fs = {}
    for ifo, f in frame_files.items():
        fs[ifo] = load_frequencyseries(f)
    return fs


def from_xml(filename, length, delta_f, low_freq_cutoff, ifo_string=None,
             root_name='psd'):
    """Read an ASCII file containing one-sided ASD or PSD  data and generate
    a frequency series with the corresponding PSD. The ASD or PSD data is
    interpolated in order to match the desired resolution of the
    generated frequency series.
    Parameters
    ----------
    filename : string
        Path to a two-column ASCII file. The first column must contain
        the frequency (positive frequencies only) and the second column
        must contain the amplitude density OR power spectral density.
    length : int
        Length of the frequency series in samples.
    delta_f : float
        Frequency resolution of the frequency series in Herz.
    low_freq_cutoff : float
        Frequencies below this value are set to zero.
    ifo_string : string
        Use the PSD in the file's PSD dictionary with this ifo string.
        If not given and only one PSD present in the file return that, if not
        given and multiple (or zero) PSDs present an exception will be raised.
    root_name : string (default='psd')
        If given use this as the root name for the PSD XML file. If this means
        nothing to you, then it is probably safe to ignore this option.
    Returns
    -------
    psd : FrequencySeries
        The generated frequency series.
    """
    import lal.series
    from glue.ligolw import utils as ligolw_utils
    from pycbc.psd import read

    fp = open(filename, 'rb')
    ct_handler = lal.series.PSDContentHandler
    fileobj, _ = ligolw_utils.load_fileobj(fp, contenthandler=ct_handler)
    psd_dict = lal.series.read_psd_xmldoc(fileobj, root_name=root_name)

    if ifo_string is not None:
        psd_freq_series = psd_dict[ifo_string]
    else:
        if len(psd_dict.keys()) == 1:
            psd_freq_series = psd_dict[tuple(psd_dict.keys())[0]]
        else:
            err_msg = "No ifo string given and input XML file contains not "
            err_msg += "exactly one PSD. Specify which PSD you want to use."
            raise ValueError(err_msg)

    noise_data = psd_freq_series.data.data[:]
    freq_data = np.arange(len(noise_data)) * psd_freq_series.deltaF

    return read.from_numpy_arrays(freq_data, noise_data, length, delta_f,
                             low_freq_cutoff)


def get_psd(strain, outdir):
    """Return the psds for each of the ifos

    Parameters
    ----------
    strain: dict
        dictionary containing the psds for each detector

    Returns
    -------
    psd: dict
        dictionary containing the psds for each detector
    """
    psd = {}
    os.system("gunzip {}/psd.xml.gz".format(outdir))
    for ifo in strain.keys():
        df = strain[ifo].delta_f
        psd[ifo] = from_xml(
            "{}/psd.xml".format(outdir),
            int(1024. / df) + 1,
            delta_f=df, low_freq_cutoff=20., ifo_string=ifo
        )
        np.savetxt(
            "{}/psd_{}.dat".format(outdir, ifo),
            np.vstack([psd[ifo].sample_frequencies, psd[ifo]]).T
        )
    return psd


def read_psd(psd_file, df):
    """Read in a psd file

    Parameters
    ----------
    strain: dict
        dictionary containing the psds for each detector
    df: float
        df to use when reading in the psd_file

    Returns
    -------
    psd_data: pycbc.frequencyseries.FrequencySeries
        data stored in the psd file
    """
    from pycbc.psd.read import from_txt

    return from_txt(psd_file, int(1024. / df) + 1, df, 20, is_asd_file=False)


def determine_approximant_to_use(template_params):
    """Decision tree to determine the which approximant to use

    Parameters
    ----------
    template_params: dict
        dictionary of the best matching template parameters

    Returns
    -------
    approximant: str
        the approximant name
    """
    mass_ratio = float(template_params["mass_1"]) / float(template_params["mass_2"])
    if mass_ratio < 18:
        approximant = "IMRPhenomD"
    else:
        approximant = "SEOBNRv4"
    return approximant


def split_data(template_params, ts, psd, f_low=20., f_high=1024., number=1):
    """Split the timeseries and psd into a series of segments

    Parameters
    ----------
    template_params: dict
        dictionary of the best matching template parameters
    f_low: float, optional
        low frequency cut-off to use for frequency splitting. Default 20.
    f_high: float, optional
        high frequency cut-off to use for frequency splitting. Default 1024.
    number: int, optional
        number of splits to make. Default 1
    """
    params_to_use = [
        template_params["mass_1"], template_params["mass_2"],
        template_params["spin_1z"], template_params["spin_2z"]
    ]
    freqs, segments = pe.split_frequency_band(params_to_use, f_low, f_high)
    maxsegl = 1.5 * np.max(segments)
    ts_ft, segment_psd, normed = pe.prepare_strain_data(
        segments, freqs, ts, template_params["gps_time"], psd
    )
    return ts_ft, segment_psd, freqs


def run_pe(
    template_params, outdir, ncpu, chunks=1, neff=1000, Dt=1., burnin=20000,
    frame_files={}, psd_file=None
):
    """Run the full workflow to generate posterior samples

    Parameters
    ----------
    template_params: dict
        dictionary of the best matching template parameters
    outdir: str
        the out directory of the run
    ncpu: int
        the number of CPUs to use for the analysis
    chunks: int
        the number of chunks to split the waveform up into
    neff: int
        the number of effective samples you wish to collect
    Dt: float
        The time window around the provided GPS within which the signal is
        coalescing
    burnin: int
        The number of samples to discard as burnin
    frame_files: dict
        dictionary of frame files to use in the analysis
    psd_file: str, dict
        path to psd.xml.gz file or dictionary of psd files to use

    Returns
    -------
    full_pe: dict
        dictionary of posterior samples
    """
    required_template_params = ["mass_1", "mass_2", "spin_1z", "spin_2z", "gps_time"]
    
    if not all(i in template_params.keys() for i in required_template_params):
        raise ValueError("Please provide all template parameters")
    template_parameters = [
        template_params[i] for i in required_template_params if i != "gps_time"
    ]
    freqs, segments = pe.split_frequency_band(template_parameters, 20., 1024.)
    maxsegl = 1.5 * np.max(segments)
    approximant = determine_approximant_to_use(template_params)
    if frame_files == {}:
        write_frequency_domain_strain(template_params, outdir, maxsegl)
    ts_ft = read_frequency_domain_strain(outdir, frame_files=frame_files)

    if psd_file is not None and isinstance(psd_file, str):
        psds = get_psd(ts_ft, psd_file)
    elif psd_file is not None and isinstance(psd_file, dict):
        psds = {}
        for ifo, path in psd_file.items():
            psds[ifo] = read_psd(path, ts_ft[ifo].delta_f)

    ts_ft, psds, freqs = split_data(
        template_params, ts_ft, psds, f_low=20., f_high=1024., number=chunks
    )
    extrinsic_mc, intrinsic_mc, lkl_thr = pe.sample_full_pe(
        ts_ft, psds, template_params["gps_time"], template_parameters,
        freqs, apx=approximant, neffective=neff, ncpu=ncpu, Dt=Dt,
        nburn=burnin
    )
    full_pe = pe.collect_posterior(extrinsic_mc, intrinsic_mc, lkl_thr)
    return full_pe


def automated_run():
    """Launch an automated run

    Returns
    -------
    full_pe: dict
        dictionary of posterior_samples
    """
    FarThr = 0.0004
    alert = json.loads(sys.stdin.read())
    template_params = respond_to_lvalert(FarThr, alert)
    if template_params != {}:
        full_pe = run_pe(
            template_params,
            "/home/charlie.hoy/projects/viabhav_fast_pe/online_pe/{}".format(
                alert['data']['graceid']
            ),
            18
        )
    return full_pe


def get_template_from_xml_file(xml_file):
    """Return the best matching template from an xml file

    Parameters
    ----------
    xml_file: str
        path to the xml file you wish to extract information from

    Returns
    -------
    template_params: dict
        dictionary of the best matching template parameters
    """
    from glue.ligolw import ligolw
    from glue.ligolw import lsctables
    from glue.ligolw import utils as ligolw_utils

    xmldoc = ligolw_utils.load_filename(
        xml_file,
        contenthandler=lsctables.use_in(ligolw.LIGOLWContentHandler)
    )
    table = lsctables.SnglInspiralTable.get_table(xmldoc)
    template_params = {
        "mass_1": table[0].mass1,
        "mass_2": table[0].mass2,
        "spin_1z": table[0].spin1z,
        "spin_2z": table[0].spin2z,
        "gps_time": table[0].end_time + 10**-9 * table[0].end_time_ns,
        "ifo": [],
        "channel": []
    }
    for row in table:
        template_params["ifo"].append(row.ifo)
        template_params["channel"].append(row.channel)
    return template_params


def download_data_from_gracedb(
    GID, outdir, download_psd=True, download_coinc=True, coinc_file=None
):
    """Download data from gracedb for a given GID

    Parameters
    ----------
    GID: str
        The GraceDB ID for an event you wish to download the data for
    outdir: str
        The directory to store the downloaded data
    download_psd: Bool
        If True, psd will be downloaded
    download_coinc: Bool
        If True, coinc file will be downloaded
    coinc_file: str
        path to coinc file

    Returns
    -------
    template_params: dict
        dictionary of the best matching template parameters
    """
    from ligo.gracedb.rest import GraceDb

    client = GraceDb()
    if download_coinc:
        xml_file = client.files(GID, "coinc.xml", raw=True).read()
        outfile = "{}/coinc.xml".format(outdir)
        with open(outfile, "wb") as f:
            f.write(xml_file)
    else:
        if coinc_file is None:
            raise ValueError(
                "Please provide a coinc file that you wish to use"
            )
        outfile = coinc_file
    template_params = get_template_from_xml_file(outfile)
    if download_psd:
        psd_file = client.files(GID, "psd.xml.gz", raw=True).read()
        outfile = "{}/psd.xml.gz".format(outdir)
        with open(outfile, "wb") as f:
            f.write(psd_file)
    return template_params


def manual_run(opts):
    """Launch a manual run

    Parameters
    ----------
    opts: 

    Returns
    -------
    full_pe: dict
        dictionary of posterior_samples
    """
    template_params = download_data_from_gracedb(
        opts.gid, opts.outdir, download_psd=opts.download_psd,
        download_coinc=opts.download_coinc, coinc_file=opts.coinc
    )
    if template_params != {}:
        full_pe = run_pe(
            template_params, opts.outdir, opts.nparallel, chunks=opts.chunks,
            neff=opts.neff, Dt=opts.dt, frame_files=opts.frame_files,
            psd_file=opts.psd_file
        )
    return full_pe


def save_to_file(full_pe, outdir):
    """Save the posterior samples to file

    Parameters
    ----------
    full_pe: dict
        dictionary of posterior_samples
    outdir: str
        output directory of the posterior_samples
    """
    full_pe["likelihood"] = np.exp(full_pe["probability"])
    full_pe["log_likelihood"] = full_pe["probability"]
    full_pe["iota"] = np.arccos(full_pe["cosi"])
    full_pe["weights"] = np.exp(full_pe["probability"] - np.max(full_pe["probability"]))
    np.savetxt(
        "{}/posterior_samples.dat".format(outdir),
        np.vstack([full_pe[i] for i in full_pe.keys()]).T,
        delimiter="\t",
        header="\t".join([parameter_name_conversion[i] for i in full_pe.keys()]),
        comments=''
    )


def post_processing(full_pe, GID, outdir, webdir):
    """Perform the post-processing of the posterior samples with PESummary

    Parameters
    ----------
    full_pe: dict
        dictionary of posterior_samples
    GID: str
        The GraceDB ID for an event you wish to download the data for
    outdir: str
        output directory of the code
    """
    psd_files = glob("{}/psd_*.dat".format(outdir))
    detectors = [i.split("psd_")[1].split(".dat")[0] for i in psd_files]
    psd_arg = ["{}:{}".format(i, j) for i, j in zip(detectors, psd_files)]
    args = "--webdir {} --gw --approximant {} --gracedb {} --psd {}".format(
        webdir, "IMRPhenomD", GID, " ".join(psd_arg)
    )
    args += " --samples {}".format(
        "%s/posterior_samples.dat" % (outdir)
    )
    os.system("summarypages {}".format(args))


def make_a_condor_job(inputs, opts):
    """Make and submit a condor job for the pipeline

    Parameters
    ----------
    inputs: argparse.Namespace
        Namespace objects containing command line arguments
    """
    from ..condor import Dag, DataFindNode, VarahaNode, PESummaryNode

    MainDag = Dag(inputs)
    MainJob = VarahaNode(inputs, opts, MainDag.output_directories, MainDag.dagman)
    PESummaryJob = PESummaryNode(inputs, MainDag.output_directories, MainDag.dagman)
    if inputs.frame_files == {}:
        DataFindJob = DataFindNode(inputs, MainDag.output_directories, MainDag.dagman)
        DataFindJob.add_child(MainJob.job)
    MainJob.add_child(PESummaryJob.job)
    MainDag.build()
    if inputs.condor_submit:
        MainDag.build_submit()
    else:
        MainDag.build()


def main():
    """The main function to execute the pipeline
    """
    from ..inputs import Inputs

    parser = command_line()
    opts = parser.parse_args()
    inputs = Inputs(opts)

    if inputs.condor:
        make_a_condor_job(inputs, opts)
        return

    main_job_imports()

    if inputs.grab_data:
        template_params = download_data_from_gracedb(inputs.gid, inputs.outdir)
        required_template_params = ["mass_1", "mass_2", "spin_1z", "spin_2z", "gps_time"]
        template_parameters = [
            template_params[i] for i in required_template_params if i != "gps_time"
        ]
        freqs, segments = pe.split_frequency_band(template_parameters, 20., 1024.)
        maxsegl = 1.5 * np.max(segments)
        write_frequency_domain_strain(template_params, inputs.outdir, maxsegl)
        return

    full_pe = manual_run(inputs)
    save_to_file(full_pe, opts.outdir)
    post_processing(full_pe, opts.gid, opts.outdir, opts.webdir)


if __name__ == "__main__":
    main()
