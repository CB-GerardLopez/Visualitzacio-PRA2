# Importar paquets

import pandas as pd
import numpy as np

# Carregar document

df = pd.read_csv("HCMST_ver_3.04.csv",low_memory=False)

# Ajustar noms de camps per legibilitat i fent "yes/no" -> 1/0 per a ser operables

df.ppethm = df.ppethm.apply(lambda x: "white" if "white" in x else "people of color")
q24 = df.filter(regex='^q24',axis=1).columns
df[q24] = df[q24].fillna(0).replace({"No":0,"Yes":1,"met online":1,"met offline":0})
df.rename(columns = {"q24_R_friend":"Friend",
"q24_bar_restaurant":"Bar/Restaurant",
"q24_R_cowork":"Work",
"q24_private_party": "Party",
"q24_school": "School",
"q24_R_family": "Family",
"q24_met_online": "Online",
"q24_college": "College"},inplace = True)

# Generació de camps d'agregació

df["Year"] = df.apply(lambda x: 10*np.floor((x.ppppcmdate_yrmo//100-x.how_long_relationship)/10),axis=1)
df["Group"] = df.apply(lambda x: x.ppethm+"/"+str(x.same_sex_couple)[:-7] if x.same_sex_couple is not np.nan else np.nan,axis=1)

# Agregació de dades i addició de camps de filtre

group = df.groupby("Group")[["Friend","Bar/Restaurant","Work","Party","School","Family","Online","College"]].agg("sum")
group = group.apply(lambda x: x/x.sum(),axis=1).round(2)
group["Filter"] = np.array(["Different sex","Same sex","Different sex","Same sex"])
year = df.groupby(["Year","same_sex_couple"])[["Friend","Bar/Restaurant","Work","Party","School","Family","Online","College"]].agg("sum").reset_index()

# Guardar taules generades

year.to_csv("year.csv")
group.to_csv("group.csv")