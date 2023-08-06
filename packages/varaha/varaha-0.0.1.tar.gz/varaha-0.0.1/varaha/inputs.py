import os


class Inputs(object):
    """Class to check the command line arguments

    Parameters
    ----------
    opts: argparse.Namespace
        Namespace object containing the command line options

    Attributes
    ----------
    opts: argparse.Namespace
        Namespace object containing the command line options
    ini: str
        Path to the varaha configuration file
    gid: str
        GraceDB event identifier for the event you wish to analyse
    nparallel: int
        The number of CPUs to use for the analysis
    chunks: int
        The number of chunks to split the waveform up into
    dt: float
        Time window around the provided GPS within which the signal is coalescing
    neff: int
        The number of effective samples you wish to collect
    burnin: int
        The number of samples to discard as burnin
    condor: Bool
        Setup a condor dag for the job
    condor_submit: Bool
        Setup and submit a condor dag for the job
    outdir: str
        Directory to store the output from varaha
    webdir: str
        Directory to store the summary pages
    grab_data: Bool
        Only query gw_data_find and return gravitational wave strain data
    types: dict
        Type of frames to look for with gw_data_find
    channels: dict
        Channels to use to read h(t) frame files
    glob_frame_data: str
        Directory to search for saved gravitational wave frame data
    frame_files: dict
        Frame files to use in the analysis
    h1_psd: str
        PSD to use for the LIGO Hanford detector
    l1_psd: str
        PSD to use for the LIGO Livingston detector
    v1_psd: str
        PSD to use for the Virgo detector
    glob_gracedb_psd: str
        Directoty to search for a saved psd.xml.gz file
    psd_file: str, dict
        psd.xml.gz file to use or dictionary of psd files to use in the analysis
    download_psd: Bool
        True if a psd.xml.gz file needs to be downloaded from GraceDB
    coinc: str
        coinc.xml file to use in the analysis
    download_coinc: Bool
        True if a coinc.xml file needs to be downloaded from GraceDB
    """
    def __init__(self, opts):
        print("Command line arguments: {}".format(opts))
        self.opts = opts
        # ini file
        self.ini = self.opts.varaha
        # Options to specify sampler settings
        self.gid = self.opts.gid
        self.nparallel = self.opts.nparallel
        self.chunks = self.opts.chunks
        self.dt = self.opts.dt
        self.neff = self.opts.neff
        self.burnin = self.opts.burnin
        # Options to specify where the save the output from varaha
        self.outdir = self.opts.outdir
        self.webdir = self.opts.webdir
        # Options specific to gravitational wave data collection
        self.grab_data = self.opts.grab_data
        self.types = self.opts.types
        self.channels = self.opts.channels
        self.glob_frame_data = self.opts.glob_frame_data
        # Options specific for PSDs
        self.h1_psd = self.opts.h1_psd
        self.l1_psd = self.opts.l1_psd
        self.v1_psd = self.opts.v1_psd
        self.glob_gracedb_psd = self.opts.glob_gracedb_psd
        self.download_psd = False
        if all(getattr(self, "{}_psd".format(i)) is None for i in ["h1", "l1", "v1"]):
            if self.glob_gracedb_psd is None:
                self.download_psd = True
        if any(getattr(self, "%s_psd" % (i)) is not None for i in ["h1", "l1", "v1"]):
            self.psd_file = {}
            if self.h1_psd is not None:
                self.psd_file["H1"] = self.h1_psd
            if self.l1_psd is not None:
                self.psd_file["L1"] = self.l1_psd
            if self.v1_psd is not None:
                self.psd_file["V1"] = self.v1_psd
        # Options specific to the trigger file
        self.coinc = self.opts.coinc
        self.download_coinc = True if self.coinc is None else False
        # Options specific to the HT Condor shedular
        self.condor = self.opts.condor
        self.condor_submit = self.opts.condor_submit
        self.accounting_group = self.opts.accounting_group
        self.accounting_group_user = self.opts.accounting_group_user
        self._ini = self.write_complete_ini_file(self.opts)

    @staticmethod
    def return_integer(obj):
        """Convert obj into an integer

        Parameters
        ----------
        obj: str, float, int
            object you wish to convert to an integer
        """
        return int(obj)

    @staticmethod
    def return_float(obj):
        """Convert obj into a float

        Parameters
        ----------
        obj: str, float, int
            object you wish to convert to a float
        """
        return float(obj)

    @staticmethod
    def make_dir(path):
        """Check to see the directory exists, if not make recursively make it

        Parameters
        ----------
        path: str
            path to directory
        """
        if not os.path.isdir(path):
            os.makedirs(path)

    @staticmethod
    def check_file_exists(path):
        """Check that a file exists. If not raise an error

        Parameters
        ----------
        path: str
            path to the file
        """
        if not os.path.isfile(path):
            raise FileNotFoundError("File {} does not exist".format(path))

    @staticmethod
    def find_files(path, identifier):
        """Find files in a given directory

        Parameters
        ----------
        path: str
            path to the directory to search in
        identifer: str
            an identifier to find the relevant files
        """
        from glob import glob

        return glob(os.path.join(path, "*{}*".format(identifier)))

    @staticmethod
    def write_complete_ini_file(opts):
        """Write a complete ini file

        Parameters
        ----------
        opts: argparse.Namespace
            Namespace object containing the command line options
        """
        import configparser

        config = configparser.ConfigParser()
        for i in Inputs.get_list_of_groups():
            config[i] = {}
        for key, item in vars(opts).items():
            group = Inputs.group_by_key(key)
            if group is None:
                pass
            else:
                config[group][key] = str(item)
        with open(os.path.join(opts.outdir, "config.ini"), 'w') as f:
            config.write(f)
        return os.path.join(opts.outdir, "config.ini")

    @staticmethod
    def group_by_key(key):
        mapping = {
            "paths": ["outdir", "webdir"],
            "analysis": ["nparallel", "chunks", "dt", "gid", "neff", "burnin"],
            "condor": [
                "condor", "condor_submit", "accounting_group", "accounting_group_user"
            ],
            "data": ["glob_frame_data", "types"],
            "psd": ["h1_psd", "l1_psd", "v1_psd", "glob_gracedb_psd"],
            "trigger": ["coinc"]
        }
        for group, item in mapping.items():
            if key in item:
                return group

    @staticmethod
    def get_list_of_groups():
        return ["paths", "analysis", "data", "psd", "trigger", "condor"]

    @property
    def ini(self):
        return self._ini

    @ini.setter
    def ini(self, ini):
        self._ini = ini
        if self._ini is not None:
            self._ini = os.path.abspath(ini)

    @property
    def gid(self):
        return self._gid

    @gid.setter
    def gid(self, gid):
        self._gid = gid
        if self._gid is not None and "G" != self._gid[0]:
            raise ValueError("Please pass a valid GraceDB event identifier")

    @property 
    def nparallel(self):
        return self._nparallel

    @nparallel.setter
    def nparallel(self, nparallel):
        self._nparallel = self.return_integer(nparallel)

    @property
    def chunks(self):
        return self._chunks

    @chunks.setter
    def chunks(self, chunks):
        self._chunks = self.return_integer(chunks)

    @property
    def dt(self):
        return self._dt

    @dt.setter
    def dt(self, dt):
        self._dt = self.return_float(dt)

    @property
    def neff(self):
        return self._neff

    @neff.setter
    def neff(self, neff):
        self._neff = self.return_integer(neff)

    @property
    def burnin(self):
        return self._burnin

    @burnin.setter
    def burnin(self, burnin):
        self._burnin = self.return_integer(burnin)

    @property
    def outdir(self):
        return self._outdir

    @outdir.setter
    def outdir(self, outdir):
        if outdir is None:
            print("Using current directory as 'outdir'")
            outdir = "."
        self.make_dir(outdir)
        self._outdir = outdir

    @property
    def webdir(self):
        return self._webdir

    @webdir.setter
    def webdir(self, webdir):
        if webdir is None:
            print("Using current directory as 'webdir'")
            webdir = "."
        self.make_dir(webdir)
        self._webdir = webdir

    @property
    def grab_data(self):
        return self._grab_data

    @grab_data.setter
    def grab_data(self, grab_data):
        self._grab_data = grab_data
        if self.gid is None:
            raise ValueError(
                "In order to query gw_data_find a GID must be provided"
            )

    @property
    def glob_frame_data(self):
        return self._glob_frame_data

    @glob_frame_data.setter
    def glob_frame_data(self, glob_frame_data):
        self._glob_frame_data = glob_frame_data
        self.frame_files = {}
        if self._glob_frame_data is not None:
            files = self.find_files(glob_frame_data, "gwf")
            if files == []:
                files = self.find_files(glob_frame_data, "hdf")
            if files == []:
                files = self.find_files(glob_frame_data, "h5")
            if files == []:
                raise ValueError(
                    "Unable to find any gravitational wave frame files in {}".format(
                        self._glob_frame_data
                    )
                )
            frame_files = {}
            for f in files:
                if "H1" in f or "H" in f:
                    frame_files["H1"] = f
                if "L1" in f or "L" in f:
                    frame_files["L1"] = f
                if "V1" in f or "V" in f:
                    frame_files["V1"] = f
            self.frame_files = frame_files

    @property
    def h1_psd(self):
        return self._h1_psd

    @h1_psd.setter
    def h1_psd(self, h1_psd):
        self._h1_psd = h1_psd
        if self._h1_psd is not None:
            self.check_file_exists(h1_psd)

    @property
    def l1_psd(self):
        return self._l1_psd

    @l1_psd.setter
    def l1_psd(self, l1_psd):
        self._l1_psd = l1_psd
        if self._l1_psd is not None:
            self.check_file_exists(l1_psd)

    @property
    def v1_psd(self):
        return self._v1_psd

    @v1_psd.setter
    def v1_psd(self, v1_psd):
        self._v1_psd = v1_psd
        if self._v1_psd is not None:
            self.check_file_exists(v1_psd)

    @property
    def glob_gracedb_psd(self):
        return self._glob_gracedb_psd

    @glob_gracedb_psd.setter
    def glob_gracedb_psd(self, glob_gracedb_psd):
        self._glob_gracedb_psd = glob_gracedb_psd
        self.psd_file = None
        if self._glob_gracedb_psd is not None:
            files = self.find_files(glob_gracedb_psd, ".xml.gz")
            if files == []:
                raise ValueError(
                    "Unable to find a psd file in {}".format(
                        self._glob_gracedb_psd
                    )
                )
            self.psd_file = files

    @property
    def coinc(self):
        return self._coinc

    @coinc.setter
    def coinc(self, coinc):
        self._coinc = coinc
        if self._coinc is not None:
            self.check_file_exists(coinc)
