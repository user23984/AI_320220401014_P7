import pandas as pd
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Fungsi interpretasi untuk mengubah nilai fuzzy menjadi label kategori
def interpretasi_tingkat_kehebatan(nilai):
    if nilai <= 40:
        return 'Kurang Bisa'
    elif nilai <= 70:
        return 'Biasa'
    else:
        return 'Hebat'

# Baca data dari file CSV
data = pd.read_excel(r"C:\path_ke\data_lari.xlsx")

# Definisikan variabel input
kecepatan_lari = ctrl.Antecedent(np.arange(3.7, 5.5, 0.1), 'kecepatan_lari')
jarak_tempuh_maksimal = ctrl.Antecedent(np.arange(5300, 8801, 100), 'jarak_tempuh_maksimal')
jarak_lari_12_menit = ctrl.Antecedent(np.arange(1500, 3201, 100), 'jarak_lari_12_menit')

# Definisikan variabel output
tingkat_kehebatan_lari = ctrl.Consequent(np.arange(0, 101, 1), 'tingkat_kehebatan_lari')

# Definisikan fungsi keanggotaan untuk variabel input dan output
kecepatan_lari.automf(3)
jarak_tempuh_maksimal.automf(3)
jarak_lari_12_menit.automf(3)

tingkat_kehebatan_lari['kurang_bisa'] = fuzz.trimf(tingkat_kehebatan_lari.universe, [0, 0, 40])
tingkat_kehebatan_lari['biasa'] = fuzz.trimf(tingkat_kehebatan_lari.universe, [30, 50, 70])
tingkat_kehebatan_lari['hebat'] = fuzz.trimf(tingkat_kehebatan_lari.universe, [60, 80, 100])

# Aturan fuzzy
rule1 = ctrl.Rule(kecepatan_lari['poor'] | jarak_tempuh_maksimal['poor'] | jarak_lari_12_menit['poor'], tingkat_kehebatan_lari['kurang_bisa'])
rule2 = ctrl.Rule(kecepatan_lari['average'] | jarak_tempuh_maksimal['average'] | jarak_lari_12_menit['average'], tingkat_kehebatan_lari['biasa'])
rule3 = ctrl.Rule(kecepatan_lari['good'] | jarak_tempuh_maksimal['good'] | jarak_lari_12_menit['good'], tingkat_kehebatan_lari['hebat'])

# Buat sistem kontrol fuzzy
tingkat_kehebatan_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
tingkat_kehebatan = ctrl.ControlSystemSimulation(tingkat_kehebatan_ctrl)

# Inisialisasi list untuk menyimpan hasil
hasil_tingkat_kehebatan = []

# Iterasi melalui setiap record dalam data
for index, row in data.iterrows():
    # Masukkan nilai variabel input dari data yang dibaca
    tingkat_kehebatan.input['kecepatan_lari'] = row['kecepatanperkm']
    tingkat_kehebatan.input['jarak_tempuh_maksimal'] = row['jarakmaksimal']
    tingkat_kehebatan.input['jarak_lari_12_menit'] = row['jarak12menit']

    # Hitung nilai variabel output
    tingkat_kehebatan.compute()

    # Simpan hasil
    hasil_tingkat_kehebatan.append(tingkat_kehebatan.output['tingkat_kehebatan_lari'])

# Tambahkan hasil ke data frame
data['hasil_tingkat_kehebatan'] = hasil_tingkat_kehebatan

# Interpretasikan nilai fuzzy menjadi kategori
data['kategori_tingkat_kehebatan'] = data['hasil_tingkat_kehebatan'].apply(interpretasi_tingkat_kehebatan)

# Simpan ke file Excel
data.to_excel('hasilfuzzynya.xlsx', index=False)
