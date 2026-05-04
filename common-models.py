import xspec

def setup_common_model():
    
    
    model = xspec.Model("tbabs * edge * (nthComp + diskbb)")

    model.tbabs.nH = "0.061, -1"
    xspec.Xset.abund = "wilm"
    xspec.Xset.xsect = "vern"

    model.edge.edgeE = "1.84, 0.01, 1.1, 1.1, 2.0, 2.0"
    model.edge.MaxTau = "0.2, 0.02, 0.0, 0.0, 2.0, 2.0"


    model.nthcomp.Gamma = "1.7, 0.01, 1.5, 1.5, 4.5, 4.5"
    model.nthcomp.kTe = "100, -1"  
    
    # kT_bb parametresini diskbb Tin'e bağla
    
    model.nthcomp.kT_bb.link = "diskbb:Tin"
    
    # inp_type: diskbb varsa 1, yoksa 0 
    model.nthcomp.inp_type = "1, -1"
    model.nthcomp.redshift = "0, -1" # Her zaman sıfır
    model.nthcomp.norm.frozen = False # Free

    # 4. diskbb: Sıcaklık ve Norm
    model.diskbb.Tin.frozen= False
    model.diskbb.norm.frozen = False

    