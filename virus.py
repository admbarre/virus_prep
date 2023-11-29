class VirusPrep():
    RATIO_TFX_OPTI = 0.033
    TFX_VOL_PER_RXN = 180 #ul
    MASTERMIX_VOL_PER_RXN = 20 #ul
    MARGIN = 1.05
    
    MASS_FRAC_PCMV = 0.88 
    MASS_FRAC_PMDG = 0.11
    MASS_FRAC_TRANSFER = 1
    
    def __init__(self,info):
        self.info = info
        self.pcmv_conc, self.pmdg_conc, self.reactions = info.values()
        self.num_rxns = len(self.reactions)
    
    def generate_instructions(self):
        instructions = [
                self.generate_tfx_mix(),
                self.generate_packaging_mix(),
                self.generate_plasmid_mix()]
        
        # TODO: we want to make this into a string instead so we can pass back up to GUI
        print("Virus Prep")
        print("---"*8)
        for block in instructions:
            for ins in block:
                print(ins)
            print("---"*8)
        print("Add transfer vector volumes to each tube.")
        print("Add 20ul of Master Mix to each tube.")
        print("Add 180ul of TFX mix to each tube.")
        print("Wait 15-60 minutes at room temperature.")
        print("Add mixture dropwise to cells.")
        
    def generate_plasmid_mix(self):
        plas_instructions = ["Transfer Vector:"]
        for rxn in self.reactions:
            name,conc = rxn
            vol = self.MASS_FRAC_TRANSFER/conc
            ins = f"+ {vol:.1f}ul {name}"
            plas_instructions.append(ins)
        return plas_instructions
    
    def generate_tfx_mix(self):
        total_vol = self.TFX_VOL_PER_RXN * self.num_rxns * self.MARGIN
        vol_tfx = total_vol * self.RATIO_TFX_OPTI
        vol_opti = total_vol - vol_tfx

        tfx_instructions = [
            f"TFX reagent Mix:",
            f"+ {vol_tfx:.2f}ul TFX",
            f"+ {vol_opti:.2f}ul Optimem"
        ]
        return tfx_instructions
    
    def generate_packaging_mix(self):
        total_vol = self.MASTERMIX_VOL_PER_RXN * self.num_rxns * self.MARGIN


        mass_pcmv = self.MASS_FRAC_PCMV * self.num_rxns * self.MARGIN
        vol_pcmv = self.get_manageable_vol("pcmv",mass_pcmv,self.pcmv_conc)

        mass_pmdg = self.MASS_FRAC_PMDG * self.num_rxns * self.MARGIN
        vol_pmdg = self.get_manageable_vol("pmdg",mass_pmdg,self.pmdg_conc)

        vol_opti = total_vol - vol_pcmv - vol_pmdg
        pack_instructions = [
            f"Packaging Master Mix:",
            f"+ {vol_pcmv:.2f}ul pCMV",
            f"+ {vol_pmdg:.2f}ul pMDG",
            f"+ {vol_opti:.2f}ul Optimem"
        ]
        return pack_instructions
    
    def get_manageable_vol(self,name,mass,conc):
        manageable_vol = 1 #ul
        add_vol = 1 #ul
        vol = mass/conc
        diluted = False

        while vol < manageable_vol:
            diluted = True
            add_vol = add_vol + 1
            new_conc = conc/(manageable_vol + add_vol)
            vol = mass/new_conc 
        if diluted:
            print(f"{name} *** Vol too small. Add {manageable_vol}ul stock plasmid to {add_vol}ul of optimem.")
            print("Use this diluted version.")
        return vol
