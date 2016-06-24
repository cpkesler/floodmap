from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import datetime
import urllib2
from tethys_sdk.gizmos import DatePicker
from tethys_sdk.gizmos import Button
from tethys_sdk.gizmos import SelectInput
from tethys_sdk.gizmos import TextInput

@login_required()
def home(request):
    """
    Controller for the app home page.
    """
    # Check digits in month and day (i.e. 2016-05-09, not 2016-5-9)
    def check_digit(num):
        num_str = str(num)
        if len(num_str) < 2:
            num_str = '0' + num_str
        return num_str

    # Find current time
    t_now = datetime.now()
    now_str = "{0}-{1}-{2}".format(t_now.year,check_digit(t_now.month),check_digit(t_now.day))

    # Gizmos
    forecast_range_select = SelectInput(display_text='Forecast Size',
                                        name='forecast_range',
                                        multiple=False,
                                        options=[ ('Short', 'short_range'), ('Medium', 'medium_range'), ('Long', 'long_range')],
                                        initial=['medium_range'],
                                        original=['medium_range'])

    forecast_date_picker = DatePicker(name='forecast_date',
                                      display_text='Forecast Date Start',
                                      end_date='0d',
                                      autoclose=True,
                                      format='yyyy-mm-dd',
                                      start_view='month',
                                      today_button=True,
                                      initial=now_str)

    forecast_time_select = SelectInput(display_text='Start Time',
                                       name='comid_time',
                                       multiple=False,
                                       options=[('12:00 am', "00"), ('1:00 am', "01"), ('2:00 am', "02"),
                                                ('3:00 am', "03"), ('4:00 am', "04"), ('5:00 am', "05"),
                                                ('6:00 am', "06"), ('7:00 am', "07"), ('8:00 am', "08"),
                                                ('9:00 am', "09"), ('10:00 am', "10"), ('11:00 am', "11"),
                                                ('12:00 pm', "12"), ('1:00 pm', "13"), ('2:00 pm', "14"),
                                                ('3:00 pm', "15"), ('4:00 pm', "16"), ('5:00 pm', "17"),
                                                ('6:00 pm', "18"), ('7:00 pm', "19"), ('8:00 pm', "20"),
                                                ('9:00 pm', "21"), ('10:00 pm', "22"), ('11:00 pm', "23")],
                                       initial=['12'],
                                       original=['12'])

    get_forecast = Button(display_text='Flood Forecast',
                           name='flood_forecast',
                           attributes='form=forecast-form',
                           submit=True)

    depth_input = TextInput(display_text='Flood Depth (meter)',
                            name='flood_depth',
                            initial='3',
                            classes='form-control')

    get_flood = Button(display_text='Chose Flood',
                          name='choose_flood',
                          attributes={""},
                          submit=True)

    get_increase = Button(display_text='Flood Increase',
                       name='flood_increase',
                       attributes='form=increase-form',
                       submit=True)

    start = request.GET.get("start", None)

    # forecast_range = 'short_range'
    # if len(forecast_range) < 0:
    #     forecast_range = 'short_range'
    #     forecast_date = '2016-06-23'
    #     comid_time = '06'
    # elif len(forecast_range) > 0:
    #     forecast_range = request.GET['forecast_range']
    #     forecast_date = request.GET['forecast_date']
    #     comid_time = request.GET['comid_time']

    # DON'T RUN THIS WHEN THE PAGE FIRST OPENS POR FAVOR
    forecast_range = request.GET['forecast_range']
    forecast_date = request.GET['forecast_date']
    comid_time = request.GET['comid_time']

    comid = '18206548'
    lag = 't00z'

    # URL for getting forecast data and in a list
    time_series_list_api = []
    if comid is not None and len(comid) > 0:
        # forecast_size = request.GET['forecast_range']
        # comid_time = "06"
        # if forecast_size == "short_range":
        #     comid_time = request.GET['comid_time']
        # print forecast_range
        print comid_time
        print comid
        print forecast_date
        forecast_date_end = now_str
        url = 'https://apps.hydroshare.org/apps/nwm-forecasts/api/GetWaterML/?config={0}&geom=channel_rt&variable=streamflow&COMID={1}&lon=&lat=&startDate={2}&endDate={3}&time={4}&lag={5}'.format(forecast_range, comid, forecast_date, forecast_date_end, comid_time, lag)
        print url
        url_api = urllib2.urlopen(url)
        data_api = url_api.read()
        # print data_api
        x = data_api.split('dateTimeUTC=')
        x.pop(0)

# MAKE ONE FOR SHORT AND ONE FOR MEDIUM RANGE BECAUSE SHORT HAS 15 VALUES WHILE MEDIUM HAS 80 VALUES
        for elm in x:
            info = elm.split(' ')
            value = info[7].split('<')
            value1 = value[0].replace('>', '')
            value2 = float(value1)
            value_round = round(value2)
            value_round_int = int(value_round)
            # print value_round_int
            if value_round_int < 1200:
                value_round_int = 1
            elif value_round_int > 1200 and value_round_int < 1400:
                value_round_int = 2
            elif value_round_int > 1400 and value_round_int < 1600:
                value_round_int = 3
            elif value_round_int > 1700 and value_round_int < 2200:
                value_round_int = 4
            elif value_round_int > 2200 and value_round_int < 2800:
                value_round_int = 5
            elif value_round_int > 2800:
                value_round_int = 6
            # NEED TO FIX THE LIST AND MAKE IT IN A SIMPLER WAY
            range_slider = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
            time_series_list_api.append(value_round_int)
            # print time_series_list_api
            range_list = zip(range_slider, time_series_list_api)
            last = range_list[-1]
            print last

        # print time_series_list_api

    context = {"forecast_range_select": forecast_range_select, "forecast_date_picker": forecast_date_picker, "forecast_time_select": forecast_time_select, "get_forecast": get_forecast, "depth_input": depth_input, "get_flood": get_flood, "get_increase": get_increase, "forecast_range": forecast_range}

    return render(request, 'floodmap/home.html', context)