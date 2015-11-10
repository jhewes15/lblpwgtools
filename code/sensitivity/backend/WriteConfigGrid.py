# Python script to write a GLoBES config, given a flux file input

# Import things
import sys, os

# Get flux file information from command line input
flux_name = sys.argv[1]
flux_fhc  = sys.argv[2]
flux_rhc  = sys.argv[3]

# Get the current working directory
workdir = os.getenv('_CONDOR_SCRATCH_DIR')

# Generate some core files
out_xsec = '{}/core/xsec.inc'.format(workdir)
f = open(out_xsec, 'w')
f.write('$version="3.2.13"\n\n')
f.write('/* Cross sections */\n')
f.write('cross(#CC)<\n')
f.write('        @cross_file = "{}/core/xsec_cc.dat"\n'.format(workdir))
f.write('>\n\n')
f.write('cross(#NC)<\n')
f.write('        @cross_file = "{}/core/xsec_nc.dat"\n'.format(workdir))
f.write('>\n')
f.close()

out_smr = '{}/core/smr.inc'.format(workdir)
f = open(out_smr, 'w')
f.write('$version="3.2.13"\n\n')
f.write('/*numu dis*/\n')
f.write('energy(#dis_nue)<>\n')
f.write('include "{}/core/LBNE_dis_smear_nue_nominal.dat"\n'.format(workdir))
f.write('energy(#dis_numu)<>\n')
f.write('include "{}/core/LBNE_dis_smear_numu_nominal.dat"\n'.format(workdir))
f.write('energy(#dis_nut)<>\n')
f.write('include "{}/core/LBNE_dis_smear_nut_nominal.dat"\n'.format(workdir))
f.write('energy(#dis_anue)<>\n')
f.write('include "{}/core/LBNE_dis_smear_anue_nominal.dat"\n'.format(workdir))
f.write('energy(#dis_anumu)<>\n')
f.write('include "{}/core/LBNE_dis_smear_anumu_nominal.dat"\n'.format(workdir))
f.write('energy(#dis_anut)<>\n')
f.write('include "{}//core/LBNE_dis_smear_anut_nominal.dat"\n'.format(workdir))
f.write('energy(#dis_NC)<>\n')
f.write('include "{}/core/LBNE_dis_smear_NC_nominal.dat"\n\n'.format(workdir))
f.write('/*nue app*/\n')
f.write('energy(#app_nue)<>\n')
f.write('include "{}/core/LBNE_app_smear_nue_nominal.dat"\n'.format(workdir))
f.write('energy(#app_numu)<>\n')
f.write('include "{}/core/LBNE_app_smear_numu_nominal.dat"\n'.format(workdir))
f.write('energy(#app_nut)<>\n')
f.write('include "{}/core/LBNE_app_smear_nut_nominal.dat"\n'.format(workdir))
f.write('energy(#app_anue)<>\n')
f.write('include "{}/core/LBNE_app_smear_anue_nominal.dat"\n'.format(workdir))
f.write('energy(#app_anumu)<>\n')
f.write('include "{}/core/LBNE_app_smear_anumu_nominal.dat"\n'.format(workdir))
f.write('energy(#app_anut)<>\n')
f.write('include "{}/core/LBNE_app_smear_anut_nominal.dat"\n'.format(workdir))
f.write('energy(#app_NC)<>\n')
f.write('include "{}/core/LBNE_app_smear_NC_nominal.dat"\n'.format(workdir))
f.close()

out_eff = '{}/core/eff.inc'.format(workdir)
f = open(out_eff, 'w')
f.write('$version="3.2.13"\n\n')
f.write('include "{}/core/GLB_app_FHC_eff.dat"\n'.format(workdir))
f.write('include "{}/core/GLB_app_RHC_eff.dat"\n'.format(workdir))
f.write('include "{}/core/GLB_dis_FHC_eff.dat"\n'.format(workdir))
f.write('include "{}/core/GLB_dis_RHC_eff.dat"\n'.format(workdir))
f.close()

# Open & write GLoBES flux .inc file
out_flux = '{}/{}.inc'.format(workdir, flux_name)
f = open(out_flux, 'w')

f.write('$version="3.1.13"\n\n')

f.write('/* Beam data */\n\n')

f.write('/*======================================================================================================*/\n')
f.write('/*                                     Beam Power Configurations                                        */\n')
f.write('/*                            (Use this chart to detemine @power in units of pot/yr)                    */\n')
f.write('/*  MI prot/pulse    Energy (GeV)    Cycle time    Beam power (MW)    Uptime&efficiency    pot/year     */\n')
f.write('/*     7.50E+13          120            1.2           1.20E+00              0.56           1.10E+21     */\n')
f.write('/*     7.50E+13           80            0.9           1.07E+00              0.56           1.47E+21     */\n')
f.write('/*     7.50E+13           60            0.7           1.03E+00              0.56           1.89E+21     */\n')
f.write('/*                                                                                                      */\n')
f.write('/*======================================================================================================*/\n\n\n')


f.write('nuflux(#flux_FHC)<\n')
f.write('  @flux_file="{}"\n'.format(flux_fhc))
f.write('  @time = 3 /* years */\n')
f.write('  @power = 10.2857 /*11.0*/  /*e20 POT per year */\n')
f.write('  @norm = 1.017718e17\n')
f.write('>\n\n')

f.write('nuflux(#flux_RHC)<\n')
f.write('  @flux_file="{}"\n'.format(flux_rhc))
f.write('  @time = 3 /* years */\n')
f.write('  @power = 10.2857 /*11.0*/  /*e20 POT per year*/\n')
f.write('  @norm = 1.017718e17\n')
f.write('>\n\n')

f.close()

# Open our GLoBES config file
out_config = '{}/{}.glb'.format(workdir, flux_name)
f = open(out_config, 'w')

f.write('%!GLoBES\n')
f.write('$version="3.2.13"\n\n')

f.write('/* Systematics Definitions */\n')
f.write('include "{}/core/definitions.inc"\n'.format(workdir))
f.write('include "{}/core/syst_list.inc"\n\n'.format(workdir))

f.write('/* Baseline */\n')
f.write('$profiletype =          1\n') 
f.write('$baseline =             1300\n')

f.write('/* Beam data */\n')
f.write('include "{}/{}.inc"\n\n'.format(workdir, flux_name))

f.write('/* Fiducial target mass [kt] */\n')
f.write('$target_mass = LAMASS\n\n\n')


f.write('/* Cross sections */\n')
f.write('include "{}/core/xsec.inc"\n\n\n'.format(workdir))


f.write('/* ----------------------------------------------------------------- */\n')
f.write('/*             Detector properties : Liquid Argon                    */\n')
f.write('/* ----------------------------------------------------------------- */\n\n')

f.write('/* Binning */\n\n')

f.write('$emin =          0.0\n')
f.write('$emax =         20.0\n')
f.write('$binsize = {0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 2.0}\n\n\n')


f.write('$sampling_min =                   0.0\n')
f.write('$sampling_max =                 110.0\n')
f.write('$sampling_stepsize = {0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 10, 10, 10, 10, 10, 10, 10, 10, 10}\n\n\n\n')



f.write('/* Technical information */\n')
f.write('$filter_state = 0\n')
f.write('$filter_value = 0.125\n\n\n')


f.write('/* Energy Resolution */\n\n')

f.write('include "{}/core/smr.inc"\n\n\n\n'.format(workdir))



f.write('/* Efficiencies */\n\n')

f.write('include "{}/core/eff.inc"\n\n'.format(workdir))

f.write('%eng = {0.0625, 0.1875, 0.3125, 0.4375, 0.5625, 0.6875, 0.8125, 0.9375, 1.0625, 1.1875, 1.3125, 1.4375, 1.5625, 1.6875, 1.8125, 1.9375, 2.0625, 2.1875, 2.3125, 2.4375, 2.5625, 2.6875, 2.8125, 2.9375, 3.0625, 3.1875, 3.3125, 3.4375, 3.5625, 3.6875, 3.8125, 3.9375, 4.0625, 4.1875, 4.3125, 4.4375, 4.5625, 4.6875, 4.8125, 4.9375, 5.0625, 5.1875, 5.3125, 5.4375, 5.5625, 5.6875, 5.8125, 5.9375, 6.0625, 6.1875, 6.3125, 6.4375, 6.5625, 6.6875, 6.8125, 6.9375, 7.0625, 7.1875, 7.3125, 7.4375, 7.5625, 7.6875, 7.8125, 7.9375, 8.0625, 8.1875, 8.3125, 8.4375, 8.5625, 8.6875, 8.8125, 8.9375, 9.0625, 9.1875, 9.3125, 9.4375, 9.5625, 9.6875, 9.8125, 9.9375, 10.0625, 10.1875, 10.3125, 10.4375, 10.5625, 10.6875, 10.8125, 10.9375, 11.0625, 11.1875, 11.3125, 11.4375, 11.5625, 11.6875, 11.8125, 11.9375, 12.0625, 12.1875, 12.3125, 12.4375, 12.5625, 12.6875, 12.8125, 12.9375, 13.0625, 13.1875, 13.3125, 13.4375, 13.5625, 13.6875, 13.8125, 13.9375, 14.0625, 14.1875, 14.3125, 14.4375, 14.5625, 14.6875, 14.8125, 14.9375, 15.0625, 15.1875, 15.3125, 15.4375, 15.5625, 15.6875, 15.8125, 15.9375, 16.0625, 16.1875, 16.3125, 16.4375, 16.5625, 16.6875, 16.8125, 16.9375, 17.0625, 17.1875, 17.3125, 17.4375, 17.5625, 17.6875, 17.8125, 17.9375, 18.0625, 18.1875, 18.3125, 18.4375, 18.5625, 18.6875, 18.8125, 18.9375, 19.0625, 19.1875, 19.3125, 19.4375, 19.5625, 19.6875, 19.8125, 19.9375}\n\n')

f.write('%sbc = samplingbincenter()\n')
f.write('%bc = bincenter()\n\n')

f.write('/* ----------------------------------------------------------------- */\n')
f.write('/*                                Channels                           */\n')
f.write('/* ----------------------------------------------------------------- */\n\n\n')


f.write('/* NUE APP */\n')
f.write('channel(#FHC_app_osc_nue)<\n')
f.write('        @channel =      #flux_FHC:     +:      m:      e:      #CC:    #app_nue\n')
f.write('        @post_smearing_efficiencies = interpolation(%eng,%post_app_FHC_nue_sig,1,%bc)\n')
f.write('>\n\n')

f.write('channel(#FHC_app_osc_nuebar)<\n')
f.write('        @channel =      #flux_FHC:     -:      m:      e:      #CC:    #app_anue\n')
f.write('        @post_smearing_efficiencies = interpolation(%eng,%post_app_FHC_nuebar_sig,1,%bc)\n')
f.write('>\n\n')

f.write('channel(#FHC_app_bkg_nue)<\n')
f.write('        @channel =      #flux_FHC:     +:      e:      e:      #CC:    #app_nue\n')
f.write('        @post_smearing_efficiencies = interpolation(%eng,%post_app_FHC_nue_bkg,1,%bc)\n')
f.write('>\n\n')

f.write('channel(#FHC_app_bkg_nuebar)<\n')
f.write('        @channel =      #flux_FHC:     -:      e:      e:      #CC:    #app_anue\n')
f.write('        @post_smearing_efficiencies = interpolation(%eng,%post_app_FHC_nuebar_bkg,1,%bc)\n')
f.write('>\n\n')

f.write('channel(#FHC_app_bkg_numu)<\n')
f.write('        @channel =      #flux_FHC:     +:      m:      m:      #CC:    #app_numu\n')
f.write('        @post_smearing_efficiencies = interpolation(%eng,%post_app_FHC_numu_bkg,1,%bc)\n')
f.write('>\n\n')

f.write('channel(#FHC_app_bkg_numubar)<\n')
f.write('        @channel =      #flux_FHC:     -:      m:      m:      #CC:    #app_anumu\n')
f.write('        @post_smearing_efficiencies = interpolation(%eng,%post_app_FHC_numubar_bkg,1,%bc)\n')
f.write('>\n\n')

f.write('channel(#FHC_app_bkg_nutau)<\n')
f.write('        @channel =      #flux_FHC:     +:      m:      t:      #CC:    #app_nut\n')
f.write('        @post_smearing_efficiencies = interpolation(%eng,%post_app_FHC_nutau_bkg,1,%bc)\n')
f.write('>\n\n')

f.write('channel(#FHC_app_bkg_nutaubar)<\n')
f.write('        @channel =      #flux_FHC:     -:      m:      t:      #CC:    #app_anut\n')
f.write('        @post_smearing_efficiencies = interpolation(%eng,%post_app_FHC_nutaubar_bkg,1,%bc)\n')
f.write('>\n\n')

f.write('channel(#FHC_app_bkg_nuNC)<\n')
f.write('        @channel =      #flux_FHC:     +:      m: NOSC_m:      #NC:    #app_NC\n')
f.write('        @post_smearing_efficiencies = interpolation(%eng,%post_app_FHC_NC_bkg,1,%bc)\n')
f.write('>\n\n')

f.write('channel(#FHC_app_bkg_nubarNC)<\n')
f.write('        @channel =      #flux_FHC:     -:      m: NOSC_m:      #NC:    #app_NC\n')
f.write('        @post_smearing_efficiencies = interpolation(%eng,%post_app_FHC_NC_bkg,1,%bc)\n')
f.write('>\n\n\n\n\n')




f.write('/* NUEBAR APP */\n')
f.write('channel(#RHC_app_osc_nue)<\n')
f.write('        @channel =      #flux_RHC:     +:      m:      e:      #CC:    #app_nue\n')
f.write('        @post_smearing_efficiencies = interpolation(%eng,%post_app_RHC_nue_sig,1,%bc)\n')
f.write('>\n\n')

f.write('channel(#RHC_app_osc_nuebar)<\n')
f.write('        @channel =      #flux_RHC:     -:      m:      e:      #CC:    #app_anue\n')
f.write('        @post_smearing_efficiencies = interpolation(%eng,%post_app_RHC_nuebar_sig,1,%bc)\n')
f.write('>\n\n')

f.write('channel(#RHC_app_bkg_nue)<\n')
f.write('        @channel =      #flux_RHC:     +:      e:      e:      #CC:    #app_nue\n')
f.write('        @post_smearing_efficiencies = interpolation(%eng,%post_app_RHC_nue_bkg,1,%bc) \n')
f.write('>\n\n')

f.write('channel(#RHC_app_bkg_nuebar)<\n')
f.write('        @channel =      #flux_RHC:     -:      e:      e:      #CC:    #app_anue\n')
f.write('        @post_smearing_efficiencies = interpolation(%eng,%post_app_RHC_nuebar_bkg,1,%bc)\n')
f.write('>\n\n')

f.write('channel(#RHC_app_bkg_numu)<\n')
f.write('        @channel =      #flux_RHC:     +:      m:      m:      #CC:    #app_numu\n')
f.write('        @post_smearing_efficiencies = interpolation(%eng,%post_app_RHC_numu_bkg,1,%bc)\n')
f.write('>\n\n')

f.write('channel(#RHC_app_bkg_numubar)<\n')
f.write('        @channel =      #flux_RHC:     -:      m:      m:      #CC:    #app_anumu\n')
f.write('        @post_smearing_efficiencies = interpolation(%eng,%post_app_RHC_numubar_bkg,1,%bc)\n')
f.write('>\n\n')

f.write('channel(#RHC_app_bkg_nutau)<\n')
f.write('        @channel =      #flux_RHC:     +:      m:      t:      #CC:    #app_nut\n')
f.write('        @post_smearing_efficiencies = interpolation(%eng,%post_app_RHC_nutau_bkg,1,%bc)\n')
f.write('>\n\n')

f.write('channel(#RHC_app_bkg_nutaubar)<\n')
f.write('        @channel =      #flux_RHC:     -:      m:      t:      #CC:    #app_anut\n')
f.write('        @post_smearing_efficiencies = interpolation(%eng,%post_app_RHC_nutaubar_bkg,1,%bc)\n')
f.write('>\n\n')

f.write('channel(#RHC_app_bkg_nuNC)<\n')
f.write('        @channel =      #flux_RHC:     +:      m: NOSC_m:      #NC:    #app_NC\n')
f.write('        @post_smearing_efficiencies = interpolation(%eng,%post_app_RHC_NC_bkg,1,%bc)\n')
f.write('>\n\n')

f.write('channel(#RHC_app_bkg_nubarNC)<\n')
f.write('        @channel =      #flux_RHC:     -:      m: NOSC_m:      #NC:    #app_NC\n')
f.write('        @post_smearing_efficiencies = interpolation(%eng,%post_app_RHC_NC_bkg,1,%bc)\n')
f.write('>\n\n\n\n\n')




f.write('/* NUMU DIS */\n')
f.write('channel(#FHC_dis_bkg_numu)<\n')
f.write('        @channel =      #flux_FHC:     +:      m:      m:      #CC:    #dis_numu\n')
f.write('        @post_smearing_efficiencies = interpolation(%eng,%post_dis_FHC_numu_bkg,1,%bc)\n')
f.write('>\n\n')

f.write('channel(#FHC_dis_bkg_numubar)<\n')
f.write('        @channel =      #flux_FHC:     -:      m:      m:      #CC:    #dis_anumu\n')
f.write('        @post_smearing_efficiencies = interpolation(%eng,%post_dis_FHC_numubar_bkg,1,%bc)\n')
f.write('>\n')

f.write('channel(#FHC_dis_bkg_nutau)<\n')
f.write('        @channel =      #flux_FHC:     +:      m:      t:      #CC:    #dis_nut\n')
f.write('        @post_smearing_efficiencies = interpolation(%eng,%post_dis_FHC_nutau_bkg,1,%bc)\n')
f.write('>\n\n')

f.write('channel(#FHC_dis_bkg_nutaubar)<\n')
f.write('        @channel =      #flux_FHC:     -:      m:      t:      #CC:    #dis_anut\n')
f.write('        @post_smearing_efficiencies = interpolation(%eng,%post_dis_FHC_nutaubar_bkg,1,%bc)\n')
f.write('>\n\n')

f.write('channel(#FHC_dis_bkg_nuNC)<\n')
f.write('        @channel =      #flux_FHC:     +:      m: NOSC_m:      #NC:    #dis_NC\n')
f.write('        @post_smearing_efficiencies = interpolation(%eng,%post_dis_FHC_NC_bkg,1,%bc)\n')
f.write('>\n\n')

f.write('channel(#FHC_dis_bkg_nubarNC)<\n')
f.write('        @channel =      #flux_FHC:     -:      m: NOSC_m:      #NC:    #dis_NC\n')
f.write('        @post_smearing_efficiencies = interpolation(%eng,%post_dis_FHC_NC_bkg,1,%bc)\n')
f.write('>\n\n\n\n\n')




f.write('/* NUMUBAR DIS */\n')
f.write('channel(#RHC_dis_bkg_numu)<\n')
f.write('        @channel =      #flux_RHC:     +:      m:      m:      #CC:    #dis_numu\n')
f.write('        @post_smearing_efficiencies = interpolation(%eng,%post_dis_RHC_numu_bkg,1,%bc)\n')
f.write('>\n\n')

f.write('channel(#RHC_dis_bkg_numubar)<\n')
f.write('        @channel =      #flux_RHC:     -:      m:      m:      #CC:    #dis_anumu\n')
f.write('        @post_smearing_efficiencies = interpolation(%eng,%post_dis_RHC_numubar_bkg,1,%bc)\n')
f.write('>\n\n')

f.write('channel(#RHC_dis_bkg_nutau)<\n')
f.write('        @channel =      #flux_RHC:     +:      m:      t:      #CC:    #dis_nut\n')
f.write('        @post_smearing_efficiencies = interpolation(%eng,%post_dis_RHC_nutau_bkg,1,%bc)\n')
f.write('>\n\n')

f.write('channel(#RHC_dis_bkg_nutaubar)<\n')
f.write('        @channel =      #flux_RHC:     -:      m:      t:      #CC:    #dis_anut\n')
f.write('        @post_smearing_efficiencies = interpolation(%eng,%post_dis_RHC_nutaubar_bkg,1,%bc)\n')
f.write('>\n\n')

f.write('channel(#RHC_dis_bkg_nuNC)<\n')
f.write('        @channel =      #flux_RHC:     +:      m: NOSC_m:      #NC:    #dis_NC\n')
f.write('        @post_smearing_efficiencies = interpolation(%eng,%post_dis_RHC_NC_bkg,1,%bc)\n')
f.write('>\n\n')

f.write('channel(#RHC_dis_bkg_nubarNC)<\n')
f.write('        @channel =      #flux_RHC:     -:      m: NOSC_m:      #NC:    #dis_NC\n')
f.write('        @post_smearing_efficiencies = interpolation(%eng,%post_dis_RHC_NC_bkg,1,%bc)\n')
f.write('>\n\n\n\n')


f.write('/* ----------------------------------------------------------------- */\n')
f.write('/*                    Rules for a Liquid Argon Detector              */\n')
f.write('/* ----------------------------------------------------------------- */\n\n')

f.write('rule(#nue_app)<\n')
f.write('        @signal = 1.0@#FHC_app_osc_nue : 1.0@#FHC_app_osc_nuebar\n')
f.write('        @sys_on_multiex_errors_sig = { #err_nue_sig } : {#err_nue_sig }\n')
f.write('        @background =  1.0@#FHC_app_bkg_nue : 1.0@#FHC_app_bkg_nuebar : 1.0@#FHC_app_bkg_numu : 1.0@#FHC_app_bkg_numubar : 1.0@#FHC_app_bkg_nutau : 1.0@#FHC_app_bkg_nutaubar : 1.0@#FHC_app_bkg_nuNC : 1.0@#FHC_app_bkg_nubarNC\n')
f.write('        @sys_on_multiex_errors_bg = {#err_nue_bg} : {#err_nue_bg} : {#err_numu_bg} : {#err_numu_bg} : {#err_nutau_bg} : {#err_nutau_bg} : {#err_numu_bg} : {#err_numu_bg}\n')
f.write('        @errordim_sys_on = 0\n')
f.write('        @errordim_sys_off = 2\n')
f.write('        @sys_on_function = "chiMultiExp"\n')
f.write('        @sys_off_function = "chiNoSysSpectrum"\n')
f.write('        @energy_window = 0.5 : 18.0\n')
f.write('>\n\n')

f.write('rule(#nuebar_app)<\n')
f.write('        @signal = 1.0@#RHC_app_osc_nue : 1.0@#RHC_app_osc_nuebar\n')
f.write('        @sys_on_multiex_errors_sig = { #err_nue_sigbar } : { #err_nue_sigbar }\n')
f.write('        @background =  1.0@#RHC_app_bkg_nue : 1.0@#RHC_app_bkg_nuebar : 1.0@#RHC_app_bkg_numu : 1.0@#RHC_app_bkg_numubar : 1.0@#RHC_app_bkg_nutau : 1.0@#RHC_app_bkg_nutaubar : 1.0@#RHC_app_bkg_nuNC : 1.0@#RHC_app_bkg_nubarNC\n')
f.write('        @sys_on_multiex_errors_bg = {#err_nue_bgbar} : {#err_nue_bgbar} : {#err_numu_bg} : {#err_numu_bg} : {#err_nutau_bg} : {#err_nutau_bg} : {#err_numu_bg} : {#err_numu_bg}\n') 
f.write('        @errordim_sys_on = 0\n')
f.write('        @errordim_sys_off = 2\n')
f.write('        @sys_on_function = "chiMultiExp"\n')
f.write('        @sys_off_function = "chiNoSysSpectrum"\n')
f.write('        @energy_window = 0.5 : 18.0\n')
f.write('>\n\n')

f.write('rule(#numu_dis)<\n')
f.write('        @signal = 1.0@#FHC_dis_bkg_numu : 1.0@#FHC_dis_bkg_numubar\n')
f.write('        @sys_on_multiex_errors_sig = { #err_numu_sig } : { #err_numu_sig }\n')
f.write('        @background = 1.0@#FHC_dis_bkg_nutau : 1.0@#FHC_dis_bkg_nutaubar : 1.0@#FHC_dis_bkg_nuNC : 1.0@#FHC_dis_bkg_nubarNC\n')
f.write('        @sys_on_multiex_errors_bg = {#err_nutau_bg} : {#err_nutau_bg} : {#err_nc_bgdis} : {#err_nc_bgdis}\n')
f.write('        @errordim_sys_on = 0\n')
f.write('        @errordim_sys_off = 2\n')
f.write('        @sys_on_function = "chiMultiExp"\n')
f.write('        @sys_off_function = "chiNoSysSpectrum"\n')
f.write('        @energy_window = 0.5 : 18.0\n')
f.write('>\n\n')

f.write('rule(#numubar_dis)<\n')
f.write('        @signal = 1.0@#RHC_dis_bkg_numu : 1.0@#RHC_dis_bkg_numubar\n')
f.write('        @sys_on_multiex_errors_sig = { #err_numu_sigbar } : { #err_numu_sigbar }\n')
f.write('        @background = 1.0@#RHC_dis_bkg_nutau : 1.0@#RHC_dis_bkg_nutaubar : 1.0@#RHC_dis_bkg_nuNC : 1.0@#RHC_dis_bkg_nubarNC\n')
f.write('        @sys_on_multiex_errors_bg = {#err_nutau_bg} : {#err_nutau_bg} : {#err_nc_bgdis} : {#err_nc_bgdis}\n')
f.write('        @errordim_sys_on = 0\n')
f.write('        @errordim_sys_off = 2\n')
f.write('        @sys_on_function = "chiMultiExp"\n')
f.write('        @sys_off_function = "chiNoSysSpectrum"\n')
f.write('        @energy_window = 0.5 : 18.0\n')
f.write('>\n\n')

f.close()

