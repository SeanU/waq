## air

cat hourly_42101_2010.csv | awk -F"," '{print $22,$19}' | sort -ur

cat hourly_42101_2010.csv | awk -F"," -v OFS='\t' '{ if($1=="\"06\"") print $1,$2,$3,$6,$7,$22,$23;}' | sort -ur

unzip -c hourly_42101_2010.zip | awk -F"," -v OFS='\t' '{ if($1=="\"06\"") print $1,$2,$3,$4,$12,$13,$14 }' | sed -e 's/\"//g'

for i in 2010 2011 2012 2013 2014 2015 2016; do unzip -c hourly_42101_$i.zip | awk -F"," -v OFS='\t' '{ if($1=="\"06\"") print $1,$2,$3,$4,$12,$13,$14 }' | sed -e 's/\"//g' > hourly_42101_$i.dat ; done

for i in 2010 2011 2012 2013 2014 2015 2016; do unzip -c hourly_42401_$i.zip | awk -F"," -v OFS='\t' '{ if($1=="\"06\"") print $1,$2,$3,$4,$12,$13,$14 }' | sed -e 's/\"//g' > hourly_42401_$i.dat ; done

for i in 2010 2011 2012 2013 2014 2015 2016; do unzip -c hourly_42602_$i.zip | awk -F"," -v OFS='\t' '{ if($1=="\"06\"") print $1,$2,$3,$4,$12,$13,$14 }' | sed -e 's/\"//g' > hourly_42602_$i.dat ; done

for i in 2010 2011 2012 2013 2014 2015 2016; do unzip -c hourly_44201_$i.zip | awk -F"," -v OFS='\t' '{ if($1=="\"06\"") print $1,$2,$3,$4,$12,$13,$14 }' | sed -e 's/\"//g' > hourly_44201_$i.dat ; done

cat hourly_42101_2010.csv | awk -F"," -v OFS='\t' '{ if($1=="\"06\"") print $1,$2,$3,$6,$7,$22,$23;}' | sort -ur

cat hourly_42101_2010.csv | awk -F"," -v OFS='\t' '{ if($1=="\"06\"") print $1,$2,$3,$6,$7,$22,$23;}' | sort -ur

for i in {2010..2016}; do unzip -c hourly_44201_$i.zip | awk -F"," -v OFS='\t' -v param=44201 -v year=$i '{ if($1=="\"06\"") print year,param,$1,$2,$3,$6,$7,$22,$23;}' | sed -e 's/\"//g' | sort -ur > lookup_44201_$i.dat; done

create external table air_hourly_parsed (state_code string, county_code string, site_num string, parameter string, date_gmt string, time_gmt string, measurement double) ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t' STORED AS TEXTFILE location '/waq/air/hourly/processed/';

## weather

for i in 2010 2011 2012 2013 2014 2015 2016; do unzip -c hourly_PRESS_$i.zip | awk -F"," -v OFS='\t' '{ if($1=="\"06\"") print $1,$2,$3,$4,$12,$13,$14 }' | sed -e 's/\"//g' > hourly_PRESS_$i.dat ; done

for i in 2010 2011 2012 2013 2014 2015 2016; do unzip -c hourly_RH_DP_$i.zip | awk -F"," -v OFS='\t' '{ if($1=="\"06\"") print $1,$2,$3,$4,$12,$13,$14 }' | sed -e 's/\"//g' > hourly_RH_DP_$i.dat ; done

for i in 2010 2011 2012 2013 2014 2015 2016; do unzip -c hourly_TEMP_$i.zip | awk -F"," -v OFS='\t' '{ if($1=="\"06\"") print $1,$2,$3,$4,$12,$13,$14 }' | sed -e 's/\"//g' > hourly_TEMP_$i.dat ; done

for i in 2010 2011 2012 2013 2014 2015 2016; do unzip -c hourly_WIND_$i.zip | awk -F"," -v OFS='\t' '{ if($1=="\"06\"") print $1,$2,$3,$4,$12,$13,$14 }' | sed -e 's/\"//g' > hourly_WIND_$i.dat ; done

create external table weather_hourly_parsed (state_code string, county_code string, site_num string, parameter string, date_gmt string, time_gmt string, measurement double) ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t' STORED AS TEXTFILE location '/waq/weather/hourly/processed/';


# merge

create external table air_weather_hourly (state_code string, county_code string, site_num string, parameter string, date_gmt string, time_gmt string, measurement double) ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t' STORED AS TEXTFILE location '/waq/air_weather_merged/hourly/';


create table air_weather_hourly_merged location '/waq/air_weather_merged/parsed' as
select state_code, county_code, site_num, date_gmt, time_gmt, 
SUM(case when parameter='42101' then measurement else 0 END) as CO,
SUM(case when parameter='42401' then measurement else 0 END) as SO2,
SUM(case when parameter='44201' then measurement else 0 END) as Ozone,
SUM(case when parameter='42602' then measurement else 0 END) as NO2,
SUM(case when parameter='64101' then measurement else 0 END) as Press,
SUM(case when parameter='62201' then measurement else 0 END) as RHDP,
SUM(case when parameter='62101' then measurement else 0 END) as Temp,
SUM(case when parameter='61103' then measurement else 0 END) as Wind
from air_weather_hourly group by state_code, county_code, site_num, date_gmt, time_gmt;