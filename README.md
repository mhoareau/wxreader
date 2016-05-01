Program to read weewx and output peet format for Xastir or other apps

Weewx stores data in MySQL, and this script reads the current weather data, outputs it in Peet format for Xastir to read and utilize for APRS weather data.


Arne format
  /* Check that user wants Arne-style broadcasts? */
  /* Using the port number as a flag */
  if (!setup_arne_udp_port && !server_arne.port) return 0 ;

  sprintf(buffer,
    "%2.1f %2.1f %2.1f %2.1f %2.1f %2.1f %d %d %3.3f %3.3f %3.3f %3.3f\r\n",
    weather_primary_T(NULL),
    wd->Tmax /*max_tempC*/,
    wd->Tmin /*min_tempC*/,
    wd->anem_mps,
    wd->anem_gust /*peak_speedMS*/,
    wd->anem_speed_max * 0.447040972 /*max_speedMS*/,
    wd->vane_bearing - 1 /*current_dir*/,
    wd->vane_mode /*max_dir*/,
    wd->rain_rate /*rain_rateI*/,
    (wd->rain >= 0.0F) ? wd->rain : 0.0,
    (wd->rain >= 0.0F) ? 0.01F * (float)
                                 (wd->rain_count - wd->rain_offset[6]) :
                         0.0F,
    (wd->rain >= 0.0F) ? 0.01F * (float)
                                 (wd->rain_count - wd->rain_offset[7]) :
                         0.0F);
 /* Perhaps we have more data? */

    if ((strlen(buffer) > nread) &&
        (9 == sscanf(&buffer[nread],
         "%f %f %f %f %f %f %f %f %d",
         &wd->RH[0],
         &RH_max,
         &RH_min,
         &wd->barom[0],
         &barom_max,
         &barom_min,
         &barom_rate,
         &wd->rain_rate,
         &check)))
    {




