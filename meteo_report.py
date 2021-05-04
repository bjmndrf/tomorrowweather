import requests as rq
import smtplib
import datetime as dt



my_email = "YOUR_EMAIL"
password = "YOUR _PASSWORD"
email_client = "EMAIL_CLIENT"
email_client_1 = "EMAIL_CLIENT_1"
email_client_2 = "EMAIL_CLIENT_2 "
client_list = [email_client, email_client_1, email_client_2]


LATITUDE = "THE_LATITUTE"
LONGITUDE = "THE_LONGITUDE"
part = "hourly"
api_key = "OPENWEATHERMAP API KEY"



OWN_endpoint = "https://api.openweathermap.org/data/2.5/onecall"
parameter = {"lat": LATITUDE,
             "lon": LONGITUDE,
             "appid": api_key,
             "exclude": "current,minutely,daily",
             "units": "metric"

             }
response = rq.get(OWN_endpoint, params=parameter)
response.raise_for_status()
weather_data = response.json()
weather_slice = weather_data["hourly"][12:24]
weather_slice_morning = weather_data["hourly"][12:18]
weather_slice_afternoon = weather_data["hourly"][19:24]
previsions_meteo = []
temperatures = []
vents = []
indices_uv = []



def temp_conditions(donnee):
    for hour_data in donnee:
        temperatures.append(hour_data["temp"])

    temp_min = min(temperatures)
    temp_max = max(temperatures)
    return [temp_min, temp_max]


def uv_conditions(data):
    for hour_data in data:

        indices_uv.append(int(hour_data["uvi"]))

    indice_uv_m = max(indices_uv)
    print(indice_uv_m)
    return indice_uv_m


def vent_conditions(data):
    for hour_data in data:
        vents.append(hour_data["wind_speed"])

        vent = max(vents)
        return (vent)


def condition_meteo(timing):
    resume_condition = []
    for hour_data in timing:
        condition_code = hour_data["weather"][0]["id"]
        if 200 <= int(condition_code) < 233:
            previsions_meteo.append("de l orage")
        elif 300 <= int(condition_code) < 323:
            previsions_meteo.append("de la pluie et brouillard")
        elif 500 <= int(condition_code) < 531:
            previsions_meteo.append("de la pluie")
        elif 600 <= int(condition_code) < 623:
            previsions_meteo.append("de la neige")
        elif int(condition_code) == 800:
            previsions_meteo.append("du grand soleil")
        elif int(condition_code) == 801:
            previsions_meteo.append("quelques rares nuages")
        elif int(condition_code) == 802:
            previsions_meteo.append("des nuages epars")
        elif int(condition_code) == 803:
            previsions_meteo.append("un ciel nuageux")
        elif int(condition_code) == 804:
            previsions_meteo.append("un ciel nuageux")
    for condition in previsions_meteo:
        if condition not in resume_condition:
            resume_condition.append(condition)
    return resume_condition


demain = " "
today = dt.date.today()
mois = " "
tomorrow = dt.date.today() + dt.timedelta(days=1)
tomorrow_day = tomorrow.strftime("%A")
current_month = tomorrow.strftime("%B")
if current_month == "April":
    mois = "Avril"
elif current_month == "May":
    mois = "Mai"
elif current_month == "June":
    mois = "Juin"
elif current_month == "July":
    mois = "Juillet"

if tomorrow_day == "Monday":
    demain = "Lundi"
elif tomorrow_day == "Tuesday":
    demain = "Mardi"
elif tomorrow_day == "Wednesday":
    demain = "Mercredi"
elif tomorrow_day == "Thursday":
    demain = "Jeudi"
elif tomorrow_day == "Friday":
    demain = "Vendredi"
elif tomorrow_day == "Saturday":
    demain = "Samedi"
elif tomorrow_day == "Sunday":
    demain = "Dimanche"

lendemain = f"{demain} {tomorrow.strftime('%d')} {mois} {tomorrow.strftime('%Y')}"

print(f"{lendemain} ")

meteo_matin = condition_meteo(weather_slice_morning)
meteo_ap_midi = condition_meteo(weather_slice_afternoon)
temp_extreme = temp_conditions(weather_slice)
print(temp_extreme)
temp_min_f = temp_extreme[0]
temp_max_f = temp_extreme[1]
vent_f = vent_conditions(weather_slice)
indice_uv_f = uv_conditions(weather_slice)

parameters_sun = {
        "lat": LATITUDE,
        "lng": LONGITUDE,
        "formatted": 1,
        "date": tomorrow.strftime('%Y-%m-%d')

    }

if int(tomorrow.strftime("%j")) <= 304:
    hour_correction = 2
else:
    hour_correction = 1


response_sun = rq.get("https://api.sunrise-sunset.org/json", params=parameters_sun)
response_sun.raise_for_status()
data_sun = response_sun.json()

sunrise_hour = int(data_sun["results"]["sunrise"].split(":")[0])
sunrise_min= data_sun["results"]["sunrise"].split(":")[1]
sunrise = f"{sunrise_hour+hour_correction}h {sunrise_min} min"

sunset_hour = int(data_sun["results"]["sunset"].split(":")[0])
sunset_min = int(data_sun["results"]["sunset"].split(":")[1])
sunset = f"{sunset_hour+hour_correction+12}h {sunset_min} min"

noon_hour = int(data_sun["results"]["solar_noon"].split(":")[0])
noon_min = int(data_sun["results"]["solar_noon"].split(":")[1])
noon = f"{noon_hour+hour_correction}h {sunset_min} min"
sun_phrase = f"Demain l'heure de l'aube est {sunrise}, le soleil sera au plus haut pour {noon} et la nuit tombera aux alentours de {sunset}."


message_matin = " ainsi que ".join(meteo_matin)
message_ap_midi = " ainsi que ".join(meteo_ap_midi)
new_text = f"{sun_phrase}\n\nLe matin il y aura {message_matin}.\n\nL' après midi il y aura {message_ap_midi}.\n\nLes températures seront  comprises entre {int(temp_min_f)} C et {int(temp_max_f)} C.\n\nLe vent soufflera à  {int(vent_f)} km/h." \
           f" \n\nL'indice UV sera au maximum de {int(indice_uv_f)} "



#
for client in client_list:
    print(client)
    with smtplib.SMTP("smtp.mail.yahoo.com", port="xxx") as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(from_addr=my_email,
                            to_addrs=client ,

                            msg=f"Subject:meteo Saint Loubes du {lendemain}\n\n"  f" {new_text} ".encode("utf-8"))
