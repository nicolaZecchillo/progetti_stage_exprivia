/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */
 
 const provinceContext = require.context(
  './istat_prov',
  false,
  /\.geojson$/
);

const provinces = provinceContext.keys().reduce((acc, fileName) => {
  const key = fileName
    .replace('./', '')
    .replace('.geojson', '')
    .replace('Com01012024_g_WGS84_', 'italy_2024_prov_');
  
  acc[key] = provinceContext(fileName);
  return acc;
}, {});

import afghanistan from './countries/afghanistan.geojson';
import albania from './countries/albania.geojson';
import algeria from './countries/algeria.geojson';
import argentina from './countries/argentina.geojson';
import australia from './countries/australia.geojson';
import austria from './countries/austria.geojson';
import belgium from './countries/belgium.geojson';
import bolivia from './countries/bolivia.geojson';
import brazil from './countries/brazil.geojson';
import bulgaria from './countries/bulgaria.geojson';
import burundi from './countries/burundi.geojson';
import canada from './countries/canada.geojson';
import chile from './countries/chile.geojson';
import china from './countries/china.geojson';
import colombia from './countries/colombia.geojson';
import costa_rica from './countries/costa_rica.geojson';
import cuba from './countries/cuba.geojson';
import cyprus from './countries/cyprus.geojson';
import denmark from './countries/denmark.geojson';
import dominican_republic from './countries/dominican_republic.geojson';
import ecuador from './countries/ecuador.geojson';
import egypt from './countries/egypt.geojson';
import el_salvador from './countries/el_salvador.geojson';
import estonia from './countries/estonia.geojson';
import ethiopia from './countries/ethiopia.geojson';
import france from './countries/france.geojson';
import france_regions from './countries/france_regions.geojson';
import finland from './countries/finland.geojson';
import germany from './countries/germany.geojson';
import guatemala from './countries/guatemala.geojson';
import haiti from './countries/haiti.geojson';
import honduras from './countries/honduras.geojson';
import iceland from './countries/iceland.geojson';
import india from './countries/india.geojson';
import indonesia from './countries/indonesia.geojson';
import iran from './countries/iran.geojson';
import italy from './countries/italy.geojson';
import italy_regions from './countries/italy_regions.geojson';
import japan from './countries/japan.geojson';
import jordan from './countries/jordan.geojson';
import kazakhstan from './countries/kazakhstan.geojson';
import kenya from './countries/kenya.geojson';
import korea from './countries/korea.geojson';
import kuwait from './countries/kuwait.geojson';
import kyrgyzstan from './countries/kyrgyzstan.geojson';
import latvia from './countries/latvia.geojson';
import liechtenstein from './countries/liechtenstein.geojson';
import lithuania from './countries/lithuania.geojson';
import malaysia from './countries/malaysia.geojson';
import mexico from './countries/mexico.geojson';
import morocco from './countries/morocco.geojson';
import myanmar from './countries/myanmar.geojson';
import netherlands from './countries/netherlands.geojson';
import nicaragua from './countries/nicaragua.geojson';
import nigeria from './countries/nigeria.geojson';
import norway from './countries/norway.geojson';
import oman from './countries/oman.geojson';
import pakistan from './countries/pakistan.geojson';
import panama from './countries/panama.geojson';
import papua_new_guinea from './countries/papua_new_guinea.geojson';
import paraguay from './countries/paraguay.geojson';
import peru from './countries/peru.geojson';
import philippines from './countries/philippines.geojson';
import portugal from './countries/portugal.geojson';
import poland from './countries/poland.geojson';
import puerto_rico from './countries/puerto_rico.geojson';
import qatar from './countries/qatar.geojson';
import russia from './countries/russia.geojson';
import rwanda from './countries/rwanda.geojson';
import saint_barthelemy from './countries/saint_barthelemy.geojson';
import saint_martin from './countries/saint_martin.geojson';
import saudi_arabia from './countries/saudi_arabia.geojson';
import singapore from './countries/singapore.geojson';
import slovenia from './countries/slovenia.geojson';
import spain from './countries/spain.geojson';
import sri_lanka from './countries/sri_lanka.geojson';
import sweden from './countries/sweden.geojson';
import switzerland from './countries/switzerland.geojson';
import syria from './countries/syria.geojson';
import tajikistan from './countries/tajikistan.geojson';
import tanzania from './countries/tanzania.geojson';
import thailand from './countries/thailand.geojson';
import timorleste from './countries/timorleste.geojson';
import turkey from './countries/turkey.geojson';
import turkmenistan from './countries/turkmenistan.geojson';
import uganda from './countries/uganda.geojson';
import uk from './countries/uk.geojson';
import ukraine from './countries/ukraine.geojson';
import united_arab_emirates from './countries/united_arab_emirates.geojson';
import uruguay from './countries/uruguay.geojson';
import usa from './countries/usa.geojson';
import uzbekistan from './countries/uzbekistan.geojson';
import venezuela from './countries/venezuela.geojson';
import vietnam from './countries/vietnam.geojson';
import zambia from './countries/zambia.geojson';
import italy_2024_municipalities from './istat_ita/Com01012024_g_WGS84.geojson';
import italy_2024_provinces from './istat_ita/ProvCM01012024_g_WGS84.geojson';
import italy_2024_regions from './istat_ita/Reg01012024_g_WGS84.geojson';
import italy_2024_districts from './istat_ita/RipGeo01012024_g_WGS84.geojson';
import italy_2024_reg_abruzzo from './istat_reg/Com01012024_g_WGS84_Abruzzo.geojson';
import italy_2024_reg_basilicata from './istat_reg/Com01012024_g_WGS84_Basilicata.geojson';
import italy_2024_reg_calabria from './istat_reg/Com01012024_g_WGS84_Calabria.geojson';
import italy_2024_reg_campania from './istat_reg/Com01012024_g_WGS84_Campania.geojson';
import italy_2024_reg_emilia_romagna from './istat_reg/Com01012024_g_WGS84_Emilia_Romagna.geojson';
import italy_2024_reg_friuli_venezia_giulia from './istat_reg/Com01012024_g_WGS84_Friuli_Venezia_Giulia.geojson';
import italy_2024_reg_lazio from './istat_reg/Com01012024_g_WGS84_Lazio.geojson';
import italy_2024_reg_liguria from './istat_reg/Com01012024_g_WGS84_Liguria.geojson';
import italy_2024_reg_lombardia from './istat_reg/Com01012024_g_WGS84_Lombardia.geojson';
import italy_2024_reg_marche from './istat_reg/Com01012024_g_WGS84_Marche.geojson';
import italy_2024_reg_molise from './istat_reg/Com01012024_g_WGS84_Molise.geojson';
import italy_2024_reg_piemonte from './istat_reg/Com01012024_g_WGS84_Piemonte.geojson';
import italy_2024_reg_puglia from './istat_reg/Com01012024_g_WGS84_Puglia.geojson';
import italy_2024_reg_sardegna from './istat_reg/Com01012024_g_WGS84_Sardegna.geojson';
import italy_2024_reg_sicilia from './istat_reg/Com01012024_g_WGS84_Sicilia.geojson';
import italy_2024_reg_toscana from './istat_reg/Com01012024_g_WGS84_Toscana.geojson';
import italy_2024_reg_trentino_alto_adige from './istat_reg/Com01012024_g_WGS84_Trentino_Alto_Adige.geojson';
import italy_2024_reg_umbria from './istat_reg/Com01012024_g_WGS84_Umbria.geojson';
import italy_2024_reg_valle_d_aosta from './istat_reg/Com01012024_g_WGS84_Valle_d_Aosta.geojson';
import italy_2024_reg_veneto from './istat_reg/Com01012024_g_WGS84_Veneto.geojson';

export const countries = {
  ...provinces,	
  italy,
  italy_regions,
  italy_2024_districts,
  italy_2024_regions,
  italy_2024_provinces,
  italy_2024_municipalities,
  italy_2024_reg_abruzzo,
  italy_2024_reg_basilicata,
  italy_2024_reg_calabria,
  italy_2024_reg_campania,
  italy_2024_reg_emilia_romagna,
  italy_2024_reg_friuli_venezia_giulia,
  italy_2024_reg_lazio,
  italy_2024_reg_liguria,
  italy_2024_reg_lombardia,
  italy_2024_reg_marche,
  italy_2024_reg_molise,
  italy_2024_reg_piemonte,
  italy_2024_reg_puglia,
  italy_2024_reg_sardegna,
  italy_2024_reg_sicilia,
  italy_2024_reg_toscana,
  italy_2024_reg_trentino_alto_adige,
  italy_2024_reg_umbria,
  italy_2024_reg_valle_d_aosta,
  italy_2024_reg_veneto,
  afghanistan,
  albania,
  algeria,
  argentina,
  australia,
  austria,
  belgium,
  bolivia,
  brazil,
  bulgaria,
  burundi,
  canada,
  chile,
  china,
  colombia,
  costa_rica,
  cuba,
  cyprus,
  denmark,
  dominican_republic,
  ecuador,
  egypt,
  el_salvador,
  estonia,
  ethiopia,
  france,
  france_regions,
  finland,
  germany,
  guatemala,
  haiti,
  honduras,
  iceland,
  india,
  indonesia,
  iran,
  italy,
  italy_regions,
  japan,
  jordan,
  kazakhstan,
  kenya,
  korea,
  kuwait,
  kyrgyzstan,
  latvia,
  liechtenstein,
  lithuania,
  malaysia,
  mexico,
  morocco,
  myanmar,
  netherlands,
  nicaragua,
  nigeria,
  norway,
  oman,
  pakistan,
  panama,
  papua_new_guinea,
  paraguay,
  peru,
  philippines,
  portugal,
  poland,
  puerto_rico,
  qatar,
  russia,
  rwanda,
  saint_barthelemy,
  saint_martin,
  saudi_arabia,
  singapore,
  slovenia,
  spain,
  sri_lanka,
  sweden,
  switzerland,
  syria,
  tajikistan,
  tanzania,
  thailand,
  timorleste,
  turkey,
  turkmenistan,
  uganda,
  uk,
  ukraine,
  united_arab_emirates,
  uruguay,
  usa,
  uzbekistan,
  venezuela,
  vietnam,
  zambia,
};

export const countryOptions = Object.keys(countries).map(x => {
  if (x === 'uk' || x === 'usa') {
    return [x, x.toUpperCase()];
  }
  if (x === 'italy_regions') {
    return [x, 'Italy (regions)'];
  }
  if (x === 'france_regions') {
    return [x, 'France (regions)'];
  }
  return [
    x,
    x
      .split('_')
      .map(e => e[0].toUpperCase() + e.slice(1))
      .join(' '),
  ];
});

export default countries;
