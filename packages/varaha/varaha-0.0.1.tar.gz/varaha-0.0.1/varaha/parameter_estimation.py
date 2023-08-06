import numpy as np
from scipy.stats import norm
from scipy.integrate import quad
import varaha.weighted_kde as wkde
from scipy.interpolate import CubicSpline, interp1d
from scipy.special import logsumexp
from scipy.stats import percentileofscore

import time
from copy import deepcopy
from multiprocessing import Pool, cpu_count
from astropy.cosmology import Planck15 as cosmo

from . import functions, detectors, gnobs

from pycbc import waveform
from pycbc.detector import Detector
from pycbc.waveform import get_fd_waveform
from pycbc.filter import sigmasq, match, matched_filter
from pycbc.filter.matchedfilter import make_frequency_series
from pycbc.psd import inverse_spectrum_truncation, interpolate

max_spin = 0.9
apx = 'IMRPhenomD'

def get_flow_for_length(template_param, length):
    
    m1_det, m2_det, s1zt, s2zt = template_param
    for f in np.arange(20., 100., 1):
        h1, _ = get_fd_waveform(approximant = apx, 
                             mass1 = m1_det, mass2 = m2_det, 
                               spin1z = s1zt, spin2z = s2zt, 
                             f_lower = f, delta_f = 1/length, f_final = 100.)
    
        idxlow = int(f * length)
        idxhigh = int((f + 10.) * length)
        phase = np.unwrap(np.angle(h1[idxlow:idxhigh]))
        dphase = np.diff(phase)

        if len(dphase[dphase < 0]) == 0:
            return np.ceil(f)
        
def get_length_for_flow(template_param, flow):
    
    m1_det, m2_det, s1zt, s2zt = template_param
    for length in np.arange(1., 1024., 1):
        h1, _ = get_fd_waveform(approximant = apx, 
                             mass1 = m1_det, mass2 = m2_det, 
                               spin1z = s1zt, spin2z = s2zt, 
                             f_lower = flow, delta_f = 1./length, f_final = 100.)
    
        idxlow = int((flow - 5) * length)
        idxhigh = int((flow + 5.) * length)
        phase = np.unwrap(np.angle(h1[idxlow:idxhigh]))
        dphase = np.diff(phase)

        if len(dphase[dphase < 0]) == 0:
            return max(16., np.ceil(length * 1.05))
        
def split_frequency_band(template_param, f_low, f_high):
    
    l0 = l = get_length_for_flow(template_param, f_low)
    segments = []
    freqs = []
    
    while l > 24.:
        segments = np.append(segments, l)
        f = get_flow_for_length(template_param, l, f_low)
        freqs = np.append(freqs, f)
        l = np.ceil(l / 2.)
  
    if l <= 24.:
        l = max(l, 16.)
        segments = np.append(segments, l)
        f = get_flow_for_length(template_param, l)
        freqs = np.append(freqs, f)
        
    freqs = np.append(freqs, f_high)
            
    return freqs, segments
        
def prepare_strain_data(split_segments, freqs, ts, gps, psd):
    
    ''' Assumes event gps lies at thr 3/4th of the segment length'''
    
    net = list(ts.keys())
    ts = deepcopy(ts)
    d = [ts[det].duration for det in net]
    if len(split_segments) > 1:
        assert len(np.unique(d)) == 1, 'Length of data for the network has unequal durations!'
        assert len(np.unique(split_segments)), 'Segments should be unique!'
    assert np.min(d) >= 24., 'To avoid data corruption minimum data duration should be 24 seconds!'
    
    ts_ft, psd_seg = {}, {}
    minf, maxf = np.min(freqs), np.max(freqs)
    for det in net:

        #tsft = ts[det].to_frequencyseries()
        tsft = ts[det]
        ts_ft[det], psd_seg[det] = [], []
        psd[det] = interpolate(psd[det], tsft.delta_f)
        tsft.resize(len(psd[det]))
        normed = (tsft / psd[det])
        idx = np.where(psd[det].data > 0)[0][0]
        
        normed[:idx] = 0
        normed = normed.to_timeseries()
        times = normed.sample_times
        t0 = times[0]

        for s in split_segments:
            idxstart = int((gps - 3./4 * s - t0)/normed.delta_t)
            idxstop = int((gps + 1./4 * s - t0)/normed.delta_t)
            
            bound = np.sign(idxstart) + np.sign(len(normed) - idxstop)
            bound += np.sign(idxstart) * np.sign(len(normed) - idxstop)
            assert bound >= 0, 'Insufficient data around event GPS!'

            ts_ft[det].append(normed[idxstart:idxstop].to_frequencyseries())
            
            psdseg = interpolate(psd[det], 1./s)
            psd_seg[det].append(psdseg)
        
    return ts_ft, psd_seg, normed 
    

def assemble_args_skyloc(signal_tilde, template_param, psd, freqs, gps = 0, Dt = 1.0, nmc_extrinsic = 1000000):
    ''' Assemble the arguments needed to perform the parameter estimation'''
    
    signal_tilde = deepcopy(signal_tilde)
    psd = deepcopy(psd)
    net_signal, net_psd = list(signal_tilde.keys()), list(psd.keys())
    assert set(net_signal) == set(net_psd), 'Non-identical network in signal/psd'
    
    net = list(signal_tilde.keys())
    fbinfinal, nseg = [], len(freqs) - 1
    m1, m2, s1z, s2z = template_param
    hptilde, langle = [], 0
    
    snrs_fiducial, flen = {}, int(np.max(freqs)/signal_tilde[net[0]][0].delta_f) + 1
    hpt, _ = get_fd_waveform(approximant=apx, mass1=m1, mass2=m2,
    spin1z=s1z, spin2z=s2z, delta_f=psd[net[0]][0].delta_f,
    f_lower=np.min(freqs), f_final = np.max(freqs) + 10)
    hpt.resize(flen)
    for det in net:
        hpsigma = sigmasq(hpt, psd = psd[det][0][:flen], 
                    low_frequency_cutoff=np.min(freqs))
        
        snrs_fiducial[det] = matched_filter(hpt, signal_tilde[det][0][:flen],
                                                    sigmasq = hpsigma,
                                   low_frequency_cutoff=np.min(freqs))
    
    for jj in range(nseg):
        hpt, _ = get_fd_waveform(approximant=apx, mass1=m1, mass2=m2,
                spin1z=s1z, spin2z=s2z, delta_f=psd[net[0]][jj].delta_f, 
                f_lower=freqs[jj], f_final = freqs[jj + 1] + 10)
        
        flen = int(freqs[jj + 1]/psd[det][jj].delta_f) + 1
        fbinfinal.append(flen)
        hpt.resize(flen)
        hpt *= np.exp(1j * langle)
        langle = np.angle(hpt[-1])
        hptilde.append(hpt)
            
        for det in net:
            psd[det][jj].resize(flen)
            signal_tilde[det][jj].resize(flen)
        
    hpsigma, snr_postfac = {}, {}
    snr_series, snr_max_det, snr_times = {}, {}, {}
    maxdetsnr = 0
    for det in net:
            
        hpsigma[det] = np.sum(sigmasq(hptilde[jj], psd = psd[det][jj], 
                    low_frequency_cutoff=freqs[jj]) for jj in range(nseg))
        
        snr_series[det] = matched_filter(hptilde[-1], signal_tilde[det][-1],
                       low_frequency_cutoff=freqs[-2], sigmasq=hpsigma[det])

        snr_times[det] = snr_series[det].sample_times
        snr_dt = snr_series[det].delta_t
        
        istart = int((gps - snr_times[det][0] - Dt) / snr_dt)
        istop = int((gps - snr_times[det][0] + Dt) / snr_dt)
        
        snr_series[det] = snr_series[det][istart:istop]
        snr_times[det] = snr_times[det][istart:istop]
        
        for ii in range(nseg - 1):
            
            cplxsnr = filter_and_sample_snr_at_tc(hptilde[ii], signal_tilde[det][ii], 
                                                      hpsigma[det],
                                                      freqs[ii], snr_times[det])
            
            snr_series[det] += cplxsnr
        
        fidtimes = snrs_fiducial[det].sample_times
        fid_istart = int((gps - fidtimes[0] - Dt) / snr_dt)
        fid_istop = int((gps - fidtimes[0] + Dt) / snr_dt)
        detsnr, snrloc  = snrs_fiducial[det][fid_istart:fid_istop].abs_max_loc()
        snr_max_det[det] = detsnr
        
        snr_split, _ = snr_series[det].abs_max_loc()
        snr_postfac[det] = detsnr / snr_split

        if detsnr > maxdetsnr:
            refdet = det
            tc_refdet = snr_times[det][snrloc]
            maxdetsnr = detsnr
            gps_istart = istart
            gps_istop = istop

    ss = np.abs(snr_series[refdet])
    sssq = ss ** 2 - np.max(ss.data) ** 2
    idxsel = np.where(sssq > - 18.)# assumes that all the probability lies beatween log-lkl of max_lkl and max_lkl - 10
    idx = idxsel[0][0] - 1
    tc_min = snr_times[refdet][idx] + ss.delta_t * (-18 - sssq[idx]) / (sssq[idx + 1] - sssq[idx])
    idx = idxsel[0][-1]
    tc_max = snr_times[refdet][idx] + ss.delta_t * (-18 - sssq[idx]) / (sssq[idx + 1] - sssq[idx])
    tc_range = [tc_min, tc_max]

    netsnr = np.sqrt(sum(snr_max_det[det] ** 2 for det in net))
    
    args_extrin = {}
    args_extrin['psd'] = psd
    args_extrin['net'] = net
    args_extrin['freqs'] = freqs
    args_extrin['fbinfinal'] = fbinfinal
    args_extrin['netsnr'] = netsnr
    args_extrin['refdet'] = refdet
    args_extrin['hpsigma'] = hpsigma 
    args_extrin['snr_times'] = snr_times 
    args_extrin['tc_refdet'] = tc_refdet
    args_extrin['gps_istart'] = gps_istart
    args_extrin['gps_istop'] = gps_istop
    args_extrin['snr_series'] = snr_series
    args_extrin['snr_max_det'] = snr_max_det
    args_extrin['signal_tilde']  = signal_tilde
    args_extrin['snr_postfac'] = snr_postfac
    
    args_extrin['nmc_extrinsic'] = nmc_extrinsic
    args_extrin['tc_range'] = tc_range
    args_extrin['phic_thr'] = 2.5/snr_max_det[refdet]
    args_extrin['snr_chisq_thr'] = 0.5 * 0.8 * netsnr ** 2
    #A large number ensures faster convergence at first cycle of extrinsic mc

    return args_extrin, snrs_fiducial

def assemble_param_ranges_extrinsic(args_extrinsic, 
                                             ra_min = 0, ra_max = 2 * np.pi, 
                                           sindec_min = -1, sindec_max = 1):
    '''Initialize parameter ranges for localising volume(extrinsic)'''
    
    refdet, netsnr = args_extrinsic['refdet'], args_extrinsic['netsnr']
    delta_t = args_extrinsic['snr_times'][refdet][1] 
    delta_t -= args_extrinsic['snr_times'][refdet][0]
    
    lumd_max = 10000
    for det in args_extrinsic['hpsigma'].keys():
        if args_extrinsic['snr_max_det'][det] > 5.:
            horizon =  np.sqrt(args_extrinsic['hpsigma'][det])
            min_noise_jittered_snr = np.sqrt(args_extrinsic['snr_max_det'][det] ** 2)
            lumd_max = min(lumd_max, horizon / min_noise_jittered_snr)
    
    lumd_min = lumd_max / 8. #see arXiv:1102.5421
    lumd_min *= (1 - 0.5 * (11/ netsnr)**2)
    lumd_max *= (1 + (11/ netsnr)**2)
    #adding extra padding -- can be made snr dependent    
    
    param_ranges = {}
    param_ranges['lumd_range'] = [[lumd_min], [lumd_max]]
    param_ranges['cosi_range'] = [[-1], [1]]
    param_ranges['ra_range'] = [[ra_min], [ra_max]]
    param_ranges['sindec_range'] = [[sindec_min], [sindec_max]]
    param_ranges['psi_range'] = [[0], [2 * np.pi]]
    
    return param_ranges

def overide_skyloc_params_with_user_given(param_ranges, ra, dec, area_on_sphere):
    ''' Over-ride a generic parameter-range dictionary with range that is 
        based on user given information.
        Currently the ranges are spread-out around user given values
        ra: float the right accession of the signal
        dec: float the declination of the signal
    '''
    #at high dec ra will also get split instead of being neither at 0 nor at 2pi - FIXME using area
    param_ranges = deepcopy(param_ranges)
    if abs(np.sin(dec)) < 0.7:
        ra_min, ra_max = ra - np.pi/4 /(netsnr/11.), ra + np.pi/4/(netsnr/11.) #FIXME -- hardcoded pi/4
    else:
        ra_min, ra_max = 0, 2 * np.pi
    param_ranges['ra_range'] = [[ra_min], [ra_max]]
    sindec_min = max(-1, np.sin(dec) - 0.5 / (netsnr/11))
    sindec_max = min(1, np.sin(dec) + 0.5 / (netsnr/11.))
    param_ranges['sindec_range'] = [[sindec_min], [sindec_max]]
    
    return param_ranges

def append_args_intrinsic(args_extrin, extrin_mc, template_param):
    
    args_intrin = deepcopy(args_extrin)
    
    net = args_extrin['net']
    tc_refdet = args_extrin['tc_refdet']
    netsnr = args_extrin['netsnr']
    
    ra_mc, dec_mc, cosi_mc = extrin_mc['ra'], extrin_mc['dec'], extrin_mc['cosi']
    psi_mc = np.random.uniform(0, 2 * np.pi, len(ra_mc))
    norm_det_mc = gnobs.get_norm_det(net, ra_mc, dec_mc, psi_mc, 0, cosi_mc, tc_refdet)
    norm_hpsigma_mc, phi_sky = {}, {}
    for det in net:
        norm_hpsigma_mc[det] = np.abs(norm_det_mc[det]) / extrin_mc['lumd']
        phi_sky[det] = np.angle(norm_det_mc[det])

    args_intrin['norm_hpsigma_mc'] = norm_hpsigma_mc
    args_intrin['phi_sky'] = phi_sky
    args_intrin['phic_thr'] = np.max(extrin_mc['phic'])
    
    dt_dets_mc = {}
    for det in net:
        dt_dets_mc[det] = detectors.time_delay_between_obs(args_extrin['refdet'], 
                                                        det, ra_mc, dec_mc, tc_refdet)
    args_intrin['dt_dets_mc'] = dt_dets_mc
    
    m1, m2, s1z, s2z = template_param
    mch, q = functions.m1m2_to_mchq(m1, m2)
    
    args_intrin['spin_max'] = 0.9
    #mch_std: 200 times the Eq 28 in arXiv:gr-qc/9402014
    mch_std = 200. * 1.2 * 1e-5 * (11/netsnr) * mch ** (8./3)
    mch_std = min(mch_std, mch ** 1.1 / 20.)
    # Here we provide phase difference between two frequencies to encapsulate time-phase consistency
    Freq = [20., 25., 100., 1000.] # FIXME *************
    args_intrin['Freq'] = Freq
    args_intrin['Psi0_fit'] = [1., 1.]
    #Maximum difference in difference of phases between 2 frequencies
    args_intrin['max_dPsi1D'] = 20.
    args_intrin['max_dPsi2D'] = 10000000.
    
    Psiatl = get_pn_phase(m1, m2, s1z, s2z, Freq[0])
    PsiatFreq = Psiatl - get_pn_phase(m1, m2, s1z, s2z, Freq[-1])
    args_intrin['Psi0'] = PsiatFreq
    
    args_intrin['mch_range'] = [[mch - 5 * mch_std], [mch + 5 * mch_std]]
    if m2/m1 < 0.2:
        args_intrin['q_range'] = [[0.05], [.25]]
    else:
        args_intrin['q_range'] = [[0.1], [1.0]]
    args_intrin['s1z_range'] = [[-max_spin], [max_spin]]
    args_intrin['s2z_range'] = [[-max_spin], [max_spin]]
    
    #print('Mass Ratio Prior', args_intrin['q_range'])
    
    return args_intrin

def override_intrinsic_ranges(args_intr, all_mch, all_q, all_s1z, all_s2z, all_lkl, lkl_thr):
    '''
       Converge in the intrinsic parameter space.
    '''
    idxsel = np.where(all_lkl > lkl_thr)

    mchsel, qsel = all_mch[idxsel], all_q[idxsel]
    s1zsel, s2zsel = all_s1z[idxsel], all_s2z[idxsel]
    m1sel, m2sel = functions.qmch_to_m1m2(mchsel, qsel)

    nbin = 5
    hist, edges = np.histogramdd((mchsel, qsel, s1zsel, s2zsel), bins = nbin)
    idx_hopeful = np.where(hist > 0)
    fracfilled = float(len(idx_hopeful[0])) / nbin ** 4
    nbin = int((len(mchsel)/50./fracfilled) ** 0.25)
    hist, edges = np.histogramdd((mchsel, qsel, s1zsel, s2zsel), bins = nbin)
    binmch, binq, bins1z, bins2z = edges
    idx_hopeful = np.where(hist > 0)

    #print('bins', nbin, len(idx_hopeful[0]), len(idxsel[0]))
    args_intr['mch_range'] = [binmch[idx_hopeful[0]],binmch[idx_hopeful[0] + 1]]
    args_intr['q_range'] = [binq[idx_hopeful[1]],binq[idx_hopeful[1] + 1]]
    args_intr['s1z_range'] = [bins1z[idx_hopeful[2]],bins1z[idx_hopeful[2] + 1]]
    args_intr['s2z_range'] = [bins2z[idx_hopeful[3]],bins2z[idx_hopeful[3] + 1]]

    flow1, fhigh1, flow2, fhigh2 = args_intr['Freq']
    Psiatl = get_pn_phase(m1sel, m2sel, s1zsel, s2zsel, flow1)
    PsiatFreq1 = Psiatl - get_pn_phase(m1sel, m2sel, s1zsel, s2zsel, fhigh1)
    Psiatl = get_pn_phase(m1sel, m2sel, s1zsel, s2zsel, flow2)
    PsiatFreq2 = Psiatl - get_pn_phase(m1sel, m2sel, s1zsel, s2zsel, fhigh2)
    z = np.polyfit(PsiatFreq1, PsiatFreq2, 1)
    dPsi = np.abs((z[0] * PsiatFreq1 + z[1] - PsiatFreq2) / z[0])

    args_intr['Psi0_fit'] = z
    args_intr['max_dPsi2D'] = np.max(dPsi)
    
    return args_intr

def get_network_time_delays(net, refdet, ra, dec, t_gps):
    ''' Get the time delays between the detectors in the network
        compared to a reference detector
    '''
    dt_dets = {}
    for det in net:
        dt_dets[det] = detectors.time_delay_between_obs(refdet, det, ra, dec, t_gps)
    
    return dt_dets

def hopeful_snrs_in_skyloc(net, snr_max_det, hpsigma_normed):
    raw_chisq = 0
    for det in net:
        raw_chisq -= hpsigma_normed[det] / 2
        raw_chisq += np.sqrt(hpsigma_normed[det]) * snr_max_det[det]
    
    return 1.2 * raw_chisq

def start_lkl_thr_from_min_match(min_match, snr_net):
    
    net, start_lkl = list(snr_net.keys()), 0
    for det in net:
         start_lkl += snr_net[det] ** 2 * (min_match - 0.5)
    
    return start_lkl

def filter_and_sample_snr_at_tc(hptld, signaltilde, hpsig, flow, snrtimes):
    
    snrseries = matched_filter(hptld, signaltilde,
                       low_frequency_cutoff=flow, sigmasq=hpsig)
    
    snr_dt = snrseries.delta_t
    times = snrseries.sample_times
    time0 = times[0]
    min_t, max_t = np.min(snrtimes.data), np.max(snrtimes.data)
    
    min_idx = ((min_t - time0)/snr_dt).astype(int) - 2
    max_idx = ((max_t - time0)/snr_dt).astype(int) + 2
    
    cplxsnr = snrseries[min_idx:max_idx]
    abssnr = np.abs(cplxsnr)
    phisnr = np.unwrap(np.angle(cplxsnr))

    abs_at_time_interp = interp1d(times[min_idx:max_idx], abssnr, kind='cubic', bounds_error = False, fill_value = 0)
    abs_at_time = abs_at_time_interp(snrtimes)
    phi_at_time = np.interp(snrtimes, times[min_idx:max_idx], phisnr)
    
    cosphi = np.cos(phi_at_time)
    resnr = abs_at_time * cosphi
    sinphi = np.sin(phi_at_time)
    imsnr = abs_at_time * sinphi
    
    cplxsnr = resnr + 1j * imsnr
    
    return cplxsnr

def snr_at_tc(net, refdet, snr_series, snr_times, tc_range, dt_dets):
    ''' Assemble the data needed to shift the time in the reference detectors
        Also calculate coalescence time in other detectors
    '''
    nsky = len(dt_dets[refdet])
    t_refdet = np.random.uniform(tc_range[0], tc_range[1], nsky)
    snr_dt = snr_series[refdet].delta_t
    snrabs_at_time, snrphi_at_time = {}, {}
    
    for det in net:
        t_det = t_refdet - dt_dets[det]
        min_t, max_t = np.min(t_det), np.max(t_det)
        min_idx = ((min_t - snr_times[det][0])/snr_dt).astype(int) - 2
        min_idx = max(0, min_idx)
        max_idx = ((max_t - snr_times[det][0])/snr_dt).astype(int) + 2
        max_idx = min(len(snr_times[det]), max_idx)
        
        cplxsnr = snr_series[det].data[min_idx:max_idx]
        
        abssnr = np.abs(cplxsnr)
        phisnr = np.unwrap(np.angle(cplxsnr))

        abs_at_time = interp1d(snr_times[det][min_idx:max_idx], abssnr, kind='cubic', bounds_error = False, fill_value = 0)
        phi_at_time = np.interp(t_det, snr_times[det][min_idx:max_idx], phisnr)
        
        snrabs_at_time[det] = abs_at_time(t_det)
        snrphi_at_time[det] = phi_at_time
     
    return snrabs_at_time, snrphi_at_time, t_refdet

def sky_likelihood(net, hpsigma_normed, snrabs_at_time, snrphi_at_time, phi_sky, phic_thr):
    
    var_term = 0
    A, B, rho_rho0 = 0, 0, {}
    for det in net:
        rho_rho0[det] = snrabs_at_time[det] * np.sqrt(hpsigma_normed[det])
        rho_rho0_sin = rho_rho0[det] * np.sin(snrphi_at_time[det] - phi_sky[det])
        rho_rho0_cos = rho_rho0[det] * np.cos(snrphi_at_time[det] - phi_sky[det])
        A += rho_rho0_sin
        B += rho_rho0_cos
        
        var_term -= hpsigma_normed[det]
    var_term *= 0.5
    
    # the sum \phi_snr -\phi_sky - 2 * \phi_c should be close to zero
    # populate phic around.
    r = np.sqrt(A ** 2 + B ** 2)
    twophic = 2 * np.random.uniform(0, phic_thr, len(hpsigma_normed[net[0]]))
    
    lkl = var_term + r * np.cos(twophic)

    return lkl, twophic / 2

def volume_localized(params_args_extrinsic):
    
    np.random.seed()
    args = deepcopy(params_args_extrinsic)
    args_extrin, param_ranges = args
    
    netsnr = args_extrin['netsnr']
    snr_max_det = args_extrin['snr_max_det']
    net, refdet = args_extrin['net'], args_extrin['refdet']
    snr_max_det = args_extrin['snr_max_det']
    hpsigma = args_extrin['hpsigma']
    snr_series, snr_times = args_extrin['snr_series'], args_extrin['snr_times']
    tc_refdet = args_extrin['tc_refdet']
    tc_range = args_extrin['tc_range']
    
    nmc_extrinsic = args_extrin['nmc_extrinsic']
    snr_chisq_thr = args_extrin['snr_chisq_thr']
    phic_thr = args_extrin['phic_thr']
    
    lumd_mins, lumd_maxs = param_ranges['lumd_range']
    cosi_mins, cosi_maxs = param_ranges['cosi_range']
    
    ra_mins, ra_maxs = param_ranges['ra_range']
    sindec_mins, sindec_maxs = param_ranges['sindec_range']
    
    psi_mins, psi_maxs = param_ranges['psi_range']
    
    lumd_mc, cosi_mc, nsamp = [], [], int(nmc_extrinsic/len(lumd_mins)) + 1
    ra_mc, dec_mc = [], []
    min_max = zip(zip(ra_mins, sindec_mins, lumd_mins, cosi_mins), 
                  zip(ra_maxs, sindec_maxs, lumd_maxs, cosi_maxs))
    
    for mins, maxs in min_max: #This is different from following loops FIXME
        ras, decs = gnobs.generate_extrinsic_sky(nsamp, ra_min = mins[0], 
                                                        ra_max = maxs[0], 
                                                    sindec_min = mins[1], 
                                                    sindec_max = maxs[1])
        ra_mc, dec_mc = np.append(ra_mc, ras), np.append(dec_mc, decs)
        lumds, cosis = gnobs.generate_extrinsic_loc(nsamp, lumd_min = mins[2], 
                                                           lumd_max = maxs[2], 
                                                           cosi_min = mins[3], 
                                                           cosi_max = maxs[3])
        lumd_mc, cosi_mc = np.append(lumd_mc, lumds), np.append(cosi_mc, cosis)        
    
    psi_mc = np.random.uniform(0, 2 * np.pi, len(ra_mc))
    norm_det_mc = gnobs.get_norm_det(net, ra_mc, dec_mc, psi_mc, 0, cosi_mc, tc_refdet)
    hpsigma_normed = {}
    for det in net:
        hpsigma_normed[det] = np.abs(norm_det_mc[det]) ** 2 * hpsigma[det] / lumd_mc ** 2
    
    #Remove samples that are confidently unlikely
    raw_lkl = hopeful_snrs_in_skyloc(net, snr_max_det, hpsigma_normed)
    idx_snrcut = np.where(raw_lkl > snr_chisq_thr)
    
    phi_sky = {}
    for det in net:
        norm_det_mc[det] = norm_det_mc[det][idx_snrcut]
        hpsigma_normed[det] = hpsigma_normed[det][idx_snrcut]
        phi_sky[det] = np.angle(norm_det_mc[det])
        
    ra_mc, dec_mc = ra_mc[idx_snrcut], dec_mc[idx_snrcut]
    lumd_mc, cosi_mc = lumd_mc[idx_snrcut], cosi_mc[idx_snrcut]
    psi_mc = psi_mc[idx_snrcut]
    
    dt_dets = get_network_time_delays(net, refdet, ra_mc, dec_mc, tc_refdet)
    snrabs_at_time, snrphi_at_time, t_uncrt = snr_at_tc(net, refdet, snr_series, snr_times, tc_range, dt_dets)
    lkl, phic_mc = sky_likelihood(net, hpsigma_normed, snrabs_at_time, snrphi_at_time, phi_sky, phic_thr)
    return [ra_mc, dec_mc, lumd_mc, cosi_mc, psi_mc, phic_mc, t_uncrt, lkl]

def localize_in_volume(args, param_ranges, neffective, stop_lkl_thr, ncpu = 1):
    '''Localize the event in volume
       args: dictionary that contains information about the signal
       param_ranges: (dictionary) ranges of sky location where MC is focused
       start_lkl_thr: float starting threshold to select samples 
       stop_lkl_thr: float stopping threshold to select samples 
       ncpu: number of cpu's to use in python multi-processing
    '''
    
    nitr = 100
    args = deepcopy(args)
    param_ranges = deepcopy(param_ranges)
    nmc_extrinsic = args['nmc_extrinsic']
    netsnr = args['netsnr']
    nbininc = eff_nbinloc = 7
    binw = binx = 7
    num_mc = nmc_extrinsic * ncpu
    ncpu = min(ncpu, cpu_count() - 2)
    pool = Pool(processes = ncpu) 
    
    assert num_mc >= 1000000, "Too few Monte Carlo samples to begin with!"
    
    #we need enough samples to start converging from
    maxl = args['snr_chisq_thr'] + stop_lkl_thr
    normdet = {}
    for itr in range(nitr):
    
        data = zip(ncpu * [args], ncpu * [param_ranges])
        results = pool.map(volume_localized, data)
    
        ra_mc = np.concatenate([yy[0] for yy in results])
        dec_mc = np.concatenate([yy[1] for yy in results])
        lumd_mc = np.concatenate([yy[2] for yy in results])
        cosi_mc = np.concatenate([yy[3] for yy in results])
        psi_mc = np.concatenate([yy[4] for yy in results])
        phic_mc = np.concatenate([yy[5] for yy in results])
        refdetdt_mc = np.concatenate([yy[6] for yy in results])
        lkl_mc = np.concatenate([yy[7] for yy in results])
        
        maxl_mc = np.max(lkl_mc)
        maxl = max(maxl, maxl_mc)
        lkl_thr = np.percentile(lkl_mc, 100 - 100. * nbininc ** 4 / len(lkl_mc))
        if lkl_thr > maxl + stop_lkl_thr:
            lkl_thr = maxl + stop_lkl_thr
        args['snr_chisq_thr'] = lkl_thr - 0.1
            
        accept_skyloc = np.where(lkl_mc > lkl_thr)
        #print(itr,')', np.round(maxl, 2), np.round(lkl_thr, 2), len(lkl_mc[accept_skyloc]),)
        
        if itr == 0:
            ra = ra_mc[accept_skyloc]
            dec = dec_mc[accept_skyloc]
            lumd = lumd_mc[accept_skyloc]
            cosi = cosi_mc[accept_skyloc]
            psi = psi_mc[accept_skyloc]
            phic = phic_mc[accept_skyloc]
            refdetdt = refdetdt_mc[accept_skyloc]
            lkl = lkl_mc[accept_skyloc]
        else:
            ra = np.append(ra[lkl > lkl_thr], ra_mc[accept_skyloc])
            dec = np.append(dec[lkl > lkl_thr], dec_mc[accept_skyloc])
            lumd = np.append(lumd[lkl > lkl_thr], lumd_mc[accept_skyloc])
            cosi = np.append(cosi[lkl > lkl_thr], cosi_mc[accept_skyloc])
            psi = np.append(psi[lkl > lkl_thr], psi_mc[accept_skyloc])
            phic = np.append(phic[lkl > lkl_thr], phic_mc[accept_skyloc])
            refdetdt = np.append(refdetdt[lkl > lkl_thr], refdetdt_mc[accept_skyloc])
            lkl = np.append(lkl[lkl > lkl_thr], lkl_mc[accept_skyloc])
        
        sindec = np.sin(dec)

        # Now converge to part of the volume that is likely
        # Identify regions with probability more than accept_prob
        
        hist, edges = np.histogramdd((ra, sindec, lumd ** 3, cosi), bins = (binw, binx, nbininc, nbininc))
        binw, binx, biny, binz = edges

        idx_hopeful = np.where(hist > 0)
        #print(len(idx_hopeful[0]))
        
        param_ranges['ra_range'] = [binw[idx_hopeful[0]], binw[idx_hopeful[0] + 1]]
        param_ranges['sindec_range'] = [binx[idx_hopeful[1]], binx[idx_hopeful[1] + 1]]
        param_ranges['lumd_range'] = [(biny[idx_hopeful[2]]) ** (1./3), (biny[idx_hopeful[2] + 1]) ** (1./3)]
        param_ranges['cosi_range'] = [binz[idx_hopeful[3]], binz[idx_hopeful[3] + 1]]

        param_ranges['psi_range'] = [np.array([-np.pi]), np.array([np.pi])]
        
        prob = np.exp(lkl - maxl)
        neff = np.sum(prob) ** 2 / np.sum(prob ** 2)
        if neff > neffective:
            break

        hist, bins = np.histogram(ra, bins = eff_nbinloc)
        idxsel = np.where(hist > len(ra) / 10)
        nbinloc = int(eff_nbinloc ** 2 / len(idxsel[0]))
        hist, bins = np.histogram(ra, bins = nbinloc)
        idxsel = np.where(hist > 0)
        binw = np.append(bins[idxsel[0]], bins[idxsel[0] + 1])
        binw = np.unique(binw)
        #print np.round(binw, 2)
        
        hist, bins = np.histogram(sindec, bins = eff_nbinloc)
        idxsel = np.where(hist > len(sindec) / 10)
        nbinloc = int(eff_nbinloc ** 2 / len(idxsel[0]))
        hist, bins = np.histogram(sindec, bins = nbinloc)
        idxsel = np.where(hist > 0)
        binx = np.append(bins[idxsel[0]], bins[idxsel[0] + 1])
        binx = np.unique(binx)
        
        args['phic_thr'] = np.max(phic)
        args['tcs_refdet'] = [np.min(refdetdt), np.max(refdetdt)]
    
    extrinsic_mc = {}
    extrinsic_mc['likelihood'] = lkl
    extrinsic_mc['psi'], extrinsic_mc['phic'] = psi, phic
    extrinsic_mc['ra'], extrinsic_mc['dec'] = ra, dec
    extrinsic_mc['lumd'], extrinsic_mc['cosi'] = lumd, cosi
    extrinsic_mc['tcs_refdet'] = refdetdt
    
    #for key in extrinsic_mc.keys():
    #    extrinsic_mc[key] = extrinsic_mc[key][-100000:]
    extrinsic_mc['prior_lumd'] = [np.min(param_ranges['lumd_range']), np.max(param_ranges['lumd_range'])]
    
    pool.close()
    
    return extrinsic_mc
        
def intrinsic_sampled(args):

    np.random.seed()

    args = deepcopy(args)

    mch_range = args['mch_range']
    q_range = args['q_range']
    s1z_range = args['s1z_range']
    s2z_range = args['s2z_range']

    net = args['net']
    netsnr = args['netsnr']
    refdet = args['refdet']
    npercpu = args['npercpu']
    freqs = args['freqs']
    fbinfinal = args['fbinfinal']

    phic_thr = args['phic_thr']
    signal_tilde, psd = args['signal_tilde'], args['psd']

    snr_max_det = args['snr_max_det']
    norm_hpsigma_mc = args['norm_hpsigma_mc']
    phi_sky = args['phi_sky']

    spin_max = args['spin_max']
  
    flow1, fhigh1, flow2, fhigh2 = args['Freq']
    Psi0 = args['Psi0']
    slp, incpt = args['Psi0_fit']
    max_dPsi1D = args['max_dPsi1D']
    max_dPsi2D = args['max_dPsi2D']

    snr_postfac = args['snr_postfac']
    snr_chisq_thr = args['snr_chisq_thr']

    dt_dets_mc = args['dt_dets_mc']

    gps_istart = args['gps_istart']
    gps_istop = args['gps_istop']
    snr_times = args['snr_times']

    ii, nseg = 0, len(freqs) - 1
    snr_chisq, dphi_hp = [], []
    mch_mc, q_mc, s1z_mc, s2z_mc = [], [], [], []
    dPsi_mc, log_sumprob_mc, skyidx_mc = [], [], []
    tcs_refdet, snr_chisq = [], []
    total_bins = len(mch_range[0])
    nthbin = np.random.randint(total_bins)

    nsky = len(dt_dets_mc[refdet])
    log_nsky = np.log(nsky)
    log_rndn = np.log(np.random.random(nsky))

    ncoll = 0
    t0 = tnow = time.time()
    while np.sign(tnow - t0 - 120.) + np.sign(ncoll - npercpu) < 2:
        nthbin = nthbin % total_bins
    
        mch = np.random.uniform(mch_range[0][nthbin], mch_range[1][nthbin])
        q = np.random.uniform(q_range[0][nthbin], q_range[1][nthbin])
        s1z = np.random.uniform(s1z_range[0][nthbin], s1z_range[1][nthbin])
        s2z = np.random.uniform(s2z_range[0][nthbin], s2z_range[1][nthbin])
    
        nthbin += 1
    
        m1, m2 = functions.qmch_to_m1m2(mch, q)
        Psiatl = get_pn_phase(m1, m2, s1z, s2z, flow1)
        PsiatFreq0 = Psiatl - get_pn_phase(m1, m2, s1z, s2z, fhigh2)
        Psiatl = get_pn_phase(m1, m2, s1z, s2z, flow1)
        PsiatFreq1 = Psiatl - get_pn_phase(m1, m2, s1z, s2z, fhigh1)
        Psiatl = get_pn_phase(m1, m2, s1z, s2z, flow2)
        PsiatFreq2 = Psiatl - get_pn_phase(m1, m2, s1z, s2z, fhigh2)
    
        dPsi1D = np.abs(PsiatFreq0 - Psi0)
        dPsi2D = np.abs((slp * PsiatFreq1 + incpt - PsiatFreq2) / slp)
    
        bound = np.sign(max_dPsi1D - dPsi1D) + np.sign(max_dPsi2D - dPsi2D)
    
    
        if bound == 2: #Hard Coded FIXME
        
            hptilde, langle = [], 0
            hpsigma, hpsigma_normed = {}, {}
            snr_series = {}
        
            for jj in range(nseg):
                hpt, _ = get_fd_waveform(approximant=apx, mass1=m1, mass2=m2,
                spin1z=s1z, spin2z=s2z, delta_f=psd[net[0]][jj].delta_f,
                f_lower=freqs[jj], f_final = freqs[jj + 1] + 10)
    
                hpt.resize(fbinfinal[jj])
                hpt *= np.exp(1j * langle)
                langle = np.angle(hpt[-1])
                hptilde.append(hpt)

            for det in net:
        
                hpsigma[det] = np.sum(sigmasq(hptilde[jj], psd = psd[det][jj],
                            low_frequency_cutoff=freqs[jj]) for jj in range(nseg))
    
                snr_series[det] = matched_filter(hptilde[-1], signal_tilde[det][-1],
                   low_frequency_cutoff=freqs[-2], sigmasq=hpsigma[det])
                hpsigma_normed[det] = norm_hpsigma_mc[det] ** 2 * hpsigma[det]

                snr_series[det] = snr_series[det][gps_istart:gps_istop]
                for jj in range(nseg - 1):
                    cplxsnr = filter_and_sample_snr_at_tc(hptilde[jj], signal_tilde[det][jj],
                                                  hpsigma[det],
                                                  freqs[jj], snr_times[det])
        
                    snr_series[det] += cplxsnr
            
                snr_series[det] *= snr_postfac[det]
            rawchisq = 0.5 * sum(np.max(np.abs(snr_series[det].data))**2 for det in net)
            if rawchisq < snr_chisq_thr:
                continue

            ss = np.abs(snr_series[refdet])
            sssq = ss ** 2 - np.max(ss.data) ** 2
            idxsel = np.where(sssq > - 18)
            idx = idxsel[0][0] - 1
            tc_min = snr_times[refdet][idx] + ss.delta_t * (-18 - sssq[idx]) / (sssq[idx + 1] - sssq[idx])
            idx = idxsel[0][-1]
            tc_max = snr_times[refdet][idx] + ss.delta_t * (-18 - sssq[idx]) / (sssq[idx + 1] - sssq[idx])
            tc_range = [tc_min, tc_max]
        
            snrabs_at_time, snrphi_at_time, tc_refdet = snr_at_tc(net, refdet, snr_series, snr_times, tc_range, dt_dets_mc)
            lkl, phics = sky_likelihood(net, hpsigma_normed, snrabs_at_time, snrphi_at_time, phi_sky, phic_thr)

            maxl = np.max(lkl)
            normed_lkl = lkl - maxl
            skyidx = np.random.choice(np.where(normed_lkl > log_rndn)[0])
            np.random.shuffle(log_rndn)
        
            mch_mc = np.append(mch_mc, mch)
            q_mc = np.append(q_mc, q)
            s1z_mc = np.append(s1z_mc, s1z)
            s2z_mc = np.append(s2z_mc, s2z)
            dPsi_mc = np.append(dPsi_mc, dPsi1D)
            log_sumprob_mc = np.append(log_sumprob_mc, logsumexp(lkl) - log_nsky)
            skyidx_mc = np.append(skyidx_mc, skyidx)
            tcs_refdet = np.append(tcs_refdet, tc_refdet[skyidx])
            snr_chisq = np.append(snr_chisq, rawchisq)
        
            ncoll += 1
        
        tnow = time.time()

    return [mch_mc, q_mc, s1z_mc, s2z_mc, dPsi_mc, log_sumprob_mc, skyidx_mc, tcs_refdet, snr_chisq]

def sample_intrinsic(args_intr, npercpu, ncpu):

    args_intr = deepcopy(args_intr)
    args_intr['npercpu'] = npercpu
    ncpu = min(ncpu, cpu_count() - 2)
    pool = Pool(processes = ncpu, maxtasksperchild = 100)
    results = pool.map(intrinsic_sampled, ncpu * [args_intr])

    mch_mc = np.concatenate([yy[0] for yy in results])
    q_mc = np.concatenate([yy[1] for yy in results])
    s1z_mc = np.concatenate([yy[2] for yy in results])
    s2z_mc = np.concatenate([yy[3] for yy in results])
    dPsi = np.concatenate([yy[4] for yy in results])
    lkl_mc = np.concatenate([yy[5] for yy in results])
    skyidx_mc = np.concatenate([yy[6] for yy in results])
    tcs_refdet = np.concatenate([yy[7] for yy in results])
    snr_chisq = np.concatenate([yy[8] for yy in results])
    
    intrinsic_mc = {}
    intrinsic_mc['mchirp'], intrinsic_mc['q'] = mch_mc, q_mc
    intrinsic_mc['spin1z'], intrinsic_mc['spin2z'] = s1z_mc, s2z_mc
    intrinsic_mc['tcs_refdet'] = tcs_refdet
    intrinsic_mc['snr_chisq'] = snr_chisq
    intrinsic_mc['dPsi'] = dPsi
    intrinsic_mc['skyidx'] = skyidx_mc
    intrinsic_mc['likelihood'] = lkl_mc
    intrinsic_mc['prior_mchirp'] = [min(args_intr['mch_range'][0]), np.max(args_intr['mch_range'][1])]
    intrinsic_mc['prior_q'] = [min(args_intr['q_range'][0]), np.max(args_intr['q_range'][1])]
    intrinsic_mc['prior_spinz'] = [-max_spin, max_spin]

    return intrinsic_mc
   
def rejection_sample(lkl, mc_dict):
    '''Perform rejection sampling on the variables contained in a dictionary
        using the provided log likelihoof.
    '''
    
    mc_dict = deepcopy(mc_dict)
    lkl -= np.max(lkl)
    prob = np.exp(lkl)
    sel_idx = np.where(prob > np.random.random(len(prob)))
    
    mc_accepted_dict = {}
    for key in mc_dict.keys():
        if key == 'likelihood':
            continue
        if 'prior' not in key:
            mc_accepted_dict[key] = mc_dict[key][sel_idx][:10000] #CHANGE ME ******
        else:
            mc_accepted_dict[key] = mc_dict[key]
        
    return mc_accepted_dict

def get_pn_phase(m1, m2, s1z, s2z, f_pn_ref):
    
    unit_norm = 4.927e-6
    mchirp, eta = functions.m1m2_to_mcheta(m1, m2)
    M, chis, chia, delta = m1 + m2, 0.5 * (s1z + s2z), 0.5 * (s1z - s2z), (m1 - m2)/(m1 + m2)
    nu, chi_pn = (np.pi * M * f_pn_ref * unit_norm) ** (1./3), chis + delta * chia - (76 * eta/113.) * chis
    
    psi1 = nu ** 2 * (3715./756 + 55.*eta/9) + nu ** 3 * (113.*chi_pn/3 - 16*np.pi)

    prefac = (3./128/eta/nu ** 5)
    
    return prefac * (1 + psi1)


def sample_full_pe(ts_ft, psd, gps, template_param, freqs, nburn=5000, ncpu=18,
                   neffective=10000, apx="IMRPhenomD", Dt=1.):
    
    # Get template waveform
    neff = 0
    apx = apx

    start_time = time.time()
    itr, maxl, lkl_thr = 0, 0, 0
    extrinsic_mc, intrinsic_mc = {}, {}
    stop_lkl_thr = -8
    perform_extrinsic = True
    nsel = 2000.
    npercpu = nsel/ncpu

    from tqdm import tqdm
    pbar = tqdm(total=neffective)
    pbar.set_description_str(
        desc="varaha neff: {} < {}".format(0, neffective), refresh=True
    )
    while neff < neffective:
        key, key_last = str(itr), str(itr - 1)
    
        if perform_extrinsic:
            args_extrinsic, _ = assemble_args_skyloc(ts_ft, template_param, psd, freqs, gps=gps, Dt=Dt)
            param_ranges = assemble_param_ranges_extrinsic(args_extrinsic)
            extrinsic_mc[key] = localize_in_volume(args_extrinsic, param_ranges, 3000, stop_lkl_thr = -10, ncpu = ncpu)
            args_intr = append_args_intrinsic(args_extrinsic, extrinsic_mc[key], template_param)
        else:
            extrinsic_mc[key] = deepcopy(extrinsic_mc[key_last])

        if itr > 0:
            args_intr = override_intrinsic_ranges(args_intr, all_mch, all_q, all_s1z, all_s2z, all_lkl, lkl_thr)
            args_intr['max_dPsi1D'] = np.max(all_dPsi[all_lkl > lkl_thr])
            args_intr['snr_chisq_thr'] = 0.99 * np.min(all_snr_chisq[all_lkl > lkl_thr])
            
        #print(itr, ')', np.round(template_param, 4))
        #print(np.min(args_intr['mch_range']), np.max((args_intr['mch_range'])))
        #print('psi fit', args_intr['Psi0_fit'])
        #print('max dpsi', args_intr['max_dPsi1D'], args_intr['max_dPsi2D'])
       
        intrinsic_mc[key] = sample_intrinsic(args_intr, npercpu, ncpu)
        lkl_mc = intrinsic_mc[key]['likelihood']
        mch_mc = intrinsic_mc[key]['mchirp']
        dPsi_mc = intrinsic_mc[key]['dPsi']
        argmaxl = np.argmax(lkl_mc)
        cycle_maxl = lkl_mc[argmaxl]
        
        if cycle_maxl - 0.1 > maxl:
            maxl = cycle_maxl
            perform_extrinsic = True
            gps = intrinsic_mc[key]['tcs_refdet'][argmaxl]
            mcht, qt = intrinsic_mc[key]['mchirp'][argmaxl], intrinsic_mc[key]['q'][argmaxl]
            s1zt, s2zt = intrinsic_mc[key]['spin1z'][argmaxl], intrinsic_mc[key]['spin2z'][argmaxl]
            m1t, m2t = functions.qmch_to_m1m2(mcht, qt)
            
            template_param = [m1t, m2t, s1zt, s2zt]
        else:
            perform_extrinsic = False
        
        keys = np.arange(min(itr, 1), itr + 1).astype(str)
        all_lkl = np.concatenate([intrinsic_mc[key]['likelihood'] for key in keys])
        all_mch = np.concatenate([intrinsic_mc[key]['mchirp'] for key in keys])
        all_q = np.concatenate([intrinsic_mc[key]['q'] for key in keys])
        all_s1z = np.concatenate([intrinsic_mc[key]['spin1z'] for key in keys])
        all_s2z = np.concatenate([intrinsic_mc[key]['spin2z'] for key in keys])
        all_dPsi = np.concatenate([intrinsic_mc[key]['dPsi'] for key in keys])
        all_snr_chisq = np.concatenate([intrinsic_mc[key]['snr_chisq'] for key in keys])
        prob = np.exp(all_lkl - np.max(all_lkl))
        neff = np.sum(prob) ** 2 / np.sum(prob ** 2)
        
        new_thr = np.percentile(all_lkl, 100 * (1 - nsel / len(all_lkl)))
        if new_thr > lkl_thr:
            lkl_thr = new_thr
        lkl_thr = min(lkl_thr, maxl + stop_lkl_thr)
    
        #print(np.round(neff, 2), np.round(maxl, 2), np.round(lkl_thr, 2), len(all_lkl[all_lkl > lkl_thr]), np.round(np.min(all_snr_chisq[all_lkl > lkl_thr]), 2))
        #print(np.round(args_intr['phic_thr'], 2), np.round(args_intr['snr_chisq_thr'], 2))
        #print()
        pbar.set_description_str(
            desc="varaha neff: {} < {}".format(int(neff), neffective), refresh=True
        )
        pbar.update(int(neff) - pbar.n)
        itr += 1
    pbar.close()
    print("---- %s seconds ----" % (time.time() - start_time))
    
    return extrinsic_mc, intrinsic_mc, lkl_thr

def collect_posterior(extrinsic_mc, intrinsic_mc, lkl_thr, first_cycle = 1):
    
    mchirp, q, spin1z, spin2z = [], [], [], []
    ra, dec, lumd, cosi = [], [], [], []
    lkl, dPsi, tcs_refdet = [], [], []
    phic = []
    lkl_extr = []
    for key in intrinsic_mc.keys():
        if float(key) < first_cycle:
            continue
        idxsel = np.where(intrinsic_mc[key]['likelihood'] > lkl_thr)
        mchirp = np.append(mchirp, intrinsic_mc[key]['mchirp'][idxsel])
        q = np.append(q, intrinsic_mc[key]['q'][idxsel])
        spin1z = np.append(spin1z, intrinsic_mc[key]['spin1z'][idxsel])
        spin2z = np.append(spin2z, intrinsic_mc[key]['spin2z'][idxsel])
        
        skyidx = intrinsic_mc[key]['skyidx'][idxsel].astype(int)
        ra = np.append(ra, extrinsic_mc[key]['ra'][skyidx])
        dec = np.append(dec, extrinsic_mc[key]['dec'][skyidx])
        lumd = np.append(lumd, extrinsic_mc[key]['lumd'][skyidx])
        cosi = np.append(cosi, extrinsic_mc[key]['cosi'][skyidx])
        phic = np.append(phic, extrinsic_mc[key]['phic'][skyidx])
        
        lkl = np.append(lkl, intrinsic_mc[key]['likelihood'][idxsel])
        dPsi = np.append(dPsi, intrinsic_mc[key]['dPsi'][idxsel])
        tcs_refdet = np.append(tcs_refdet, intrinsic_mc[key]['tcs_refdet'][idxsel])
        
        lkl_extr = np.append(lkl_extr, extrinsic_mc[key]['likelihood'][skyidx])
    
    full_pe = {}
    full_pe['mchirp'] = mchirp
    full_pe['q'] = q
    full_pe['spin1z'] = spin1z
    full_pe['spin2z'] = spin2z
    full_pe['ra'] = ra
    full_pe['dec'] = dec
    full_pe['lumd'] = lumd
    full_pe['cosi'] = cosi
    full_pe['phic'] = phic
    
    full_pe['probability'] = lkl
    full_pe['dPsi'] = dPsi
    full_pe['tcs_refdet'] = tcs_refdet
    
    full_pe['lkl_extr'] = lkl_extr
    
    return full_pe
