import pandas as pd
import os

# KAYNAK ve DOSYA TANIMI
SOURCES = {
    "MAXIJ1820p070": {
        "source":   "MAXIJ1820p070",
        "outburst_year": 2018,
        "model": "/cdata1/senaozgur/nicer/MAXIJ1820p070/nicer_automatic/commonFiles/results/model_tables",
        "flux":  "/cdata1/senaozgur/nicer/MAXIJ1820p070/nicer_automatic/commonFiles/results/flux_tables",
        "radio": "/cdata1/senaozgur/nicer/MAXIJ1820p070/radio_data/meerkat-amila.txt",
        "optic": "/cdata1/senaozgur/nicer/MAXIJ1820p070/optic_data/lco.txt",
        "states": {
            "hard":   "model_hard_98.txt",
            "hims":   "model_hims_99.txt",
            "soft": "model_soft_95.txt",
            "hims_decay": "model_hims_decay_101.txt",
        }
    },
    "SWIFTJ1753": {
        "source":        "SWIFTJ1753",
        "outburst_year": 2005,
        "model": "/cdata1/senaozgur/nicer/SWIFTJ1753/.../model_tables",
        "flux":  "/cdata1/senaozgur/nicer/SWIFTJ1753/.../flux_tables",
        "radio": "/cdata1/senaozgur/nicer/SWIFTJ1753/radio_data/radio_data.txt",
        "optic": "/cdata1/senaozgur/nicer/SWIFTJ1753/optic_data/lco.txt",  
        "states": {
            "hard":   "model_hard_45.txt",
            "soft":  "model_soft_32.txt",
        },
    },
}

# Verileri toplamak için listeler
all_model_dfs = []
all_flux_dfs  = []
all_radio_dfs = []
all_optic_dfs = []

for source_key, info in SOURCES.items():
    
    # Model ve flux verileri için
    for state, filename in info["states"].items():
        # Model tablosu 
        model_path = os.path.join(info["model"], filename)
        if os.path.exists(model_path):
            df = pd.read_csv(model_path, sep=r"\s+")
            df["source"] = info["source"]
            df["state"]  = state
            df["outburst_year"] = info["outburst_year"]
            all_model_dfs.append(df)
            
        
        # x ray Flux tablosu 
        flux_path = os.path.join(info["flux"], filename)
        if os.path.exists(flux_path):
            df = pd.read_csv(flux_path, sep=r"\s+")
            df["source"]  = info["source"]
            df["state"]  = state
            df["outburst_year"] = info["outburst_year"]
            all_flux_dfs.append(df)
            
    
    # Radyo verisi ekleme
    radio_path = info.get("radio")
    if radio_path and os.path.exists(radio_path):
        df_radio = pd.read_csv(radio_path, sep=",", comment='#')
        df_radio.columns = [col.strip() for col in df_radio.columns]
        df_radio["source"] = info["source"]
        df_radio["outburst_year"] = info["outburst_year"]
        all_radio_dfs.append(df_radio)
        
    
    # Optik verisi ekleme
    optic_path = info.get("optic")
    if optic_path and os.path.exists(optic_path):
        df_optic = pd.read_csv(optic_path, sep=",", comment='#')
        df_optic.columns = [col.strip() for col in df_optic.columns]
        df_optic["source"] = info["source"]
        df_optic["outburst_year"] = info["outburst_year"]
        all_optic_dfs.append(df_optic)
        

# Tüm verileri birleştir

df_model_all = pd.concat(all_model_dfs, ignore_index=True) if all_model_dfs else pd.DataFrame()
df_flux_all  = pd.concat(all_flux_dfs, ignore_index=True) if all_flux_dfs else pd.DataFrame()
df_radio_all = pd.concat(all_radio_dfs, ignore_index=True) if all_radio_dfs else pd.DataFrame()
df_optic_all = pd.concat(all_optic_dfs, ignore_index=True) if all_optic_dfs else pd.DataFrame()



# HDF5'e kaydet

with pd.HDFStore("nicer_all_sources.h5") as store:
    store["model"] = df_model_all
    store["flux"]  = df_flux_all
    if not df_radio_all.empty:
        store["radio"] = df_radio_all
    if not df_optic_all.empty:
        store["optic"] = df_optic_all


with pd.HDFStore("nicer_all_sources.h5") as store:
    df_model = store["model"]
    df_flux  = store["flux"]
    df_radio = store["radio"] if "/radio" in store.keys() else pd.DataFrame()
    df_optic = store["optic"] if "/optic" in store.keys() else pd.DataFrame()

# Radyo verisi kontrolü

print(df_radio[df_radio["source"] == "MAXIJ1820p070"].head())

#optik veri
print(df_optic[df_optic["source"] == "MAXIJ1820p070"].head())
    
    
