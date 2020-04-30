
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import nmc_met_map.lib.utility as utl
from datetime import datetime, timedelta
import pandas as pd
import locale
import sys
import metpy.calc as mpcalc
from metpy.plots import  SkewT
import os
from mpl_toolkits.axisartist.parasite_axes import HostAxes, ParasiteAxes
from matplotlib.ticker import MultipleLocator
import math

def draw_Station_Synthetical_Forecast_From_Cassandra(
            t2m=None,Td2m=None,AT=None,u10m=None,v10m=None,u100m=None,v100m=None,
            gust10m=None,wsp10m=None,wsp100m=None,r03=None,TCDC=None,LCDC=None,
            draw_VIS=False,VIS=None,drw_thr=False,
            time_all=None,
            model=None,points=None,
            output_dir=None,extra_info={
            'output_head_name':' ',
            'output_tail_name':' ',
            'point_name':' ',
            'upper_wind':False,
            'upper_wind_lev':'800'}):

    #if(sys.platform[0:3] == 'win'):
    plt.rcParams['font.sans-serif'] = ['SimHei'] # 步骤一（替换sans-serif字体）
    plt.rcParams['axes.unicode_minus'] = False  # 步骤二（解决坐标轴负数的负号显示问题）
    if(sys.platform[0:3] == 'lin'):
        locale.setlocale(locale.LC_CTYPE, 'zh_CN.utf8')
    if(sys.platform[0:3] == 'win'):        
        locale.setlocale(locale.LC_CTYPE, 'chinese')       

    initTime1=pd.to_datetime(str(t2m['forecast_reference_time'].values)).replace(tzinfo=None).to_pydatetime()
    initTime2=pd.to_datetime(str(VIS['forecast_reference_time'].values)).replace(tzinfo=None).to_pydatetime()

    # draw figure
    fig=plt.figure(figsize=(12,16))
    # draw main figure
    #温度————————————————————————————————————————————————
    ax = plt.axes([0.05,0.83,.94,.15])
    utl.add_public_title_sta(title=model+'预报 '+extra_info['point_name']+' ['+str(points['lon'][0])+','+str(points['lat'][0])+']',initTime=initTime1, fontsize=23)

    for ifhour in t2m['forecast_period'].values:
        if (ifhour == t2m['forecast_period'].values[0] ):
            t2m_t=(initTime1
                +timedelta(hours=ifhour))
        else:
            t2m_t=np.append(t2m_t,
                            (initTime1
                            +timedelta(hours=ifhour)))
    #开启自适应
    xaxis_intaval=mpl.dates.HourLocator(byhour=(8,20)) #单位是小时
    ax.xaxis.set_major_locator(xaxis_intaval)
    ax.set_xticklabels([' '])
    ax.fill_between(t2m_t, np.squeeze(t2m['data']), -100,facecolor='#3D5AFE')
    ax.fill_between(t2m_t, np.squeeze(t2m['data']), -5,facecolor='#2979FF')
    ax.fill_between(t2m_t, np.squeeze(t2m['data']), 0,facecolor='#00B0FF')
    ax.fill_between(t2m_t, np.squeeze(t2m['data']), 5,facecolor='#00E5FF')
    ax.fill_between(t2m_t, np.squeeze(t2m['data']), 13,facecolor='#1DE9B6')
    ax.fill_between(t2m_t, np.squeeze(t2m['data']), 18,facecolor='#00E676')
    ax.fill_between(t2m_t, np.squeeze(t2m['data']), 22,facecolor='#76FF03')
    ax.fill_between(t2m_t, np.squeeze(t2m['data']), 28,facecolor='#C6FF00')
    ax.fill_between(t2m_t, np.squeeze(t2m['data']), 33,facecolor='#FFEA00')
    ax.fill_between(t2m_t, np.squeeze(t2m['data']), 35,facecolor='#FFC400')
    ax.fill_between(t2m_t, np.squeeze(t2m['data']), 37,facecolor='#FF9100')
    ax.fill_between(t2m_t, np.squeeze(t2m['data']), 40,facecolor='#FF3D00')
    ax.fill_between(t2m_t, np.squeeze(t2m['data']), 100,facecolor='#FFFFFF')
    ax.plot(t2m_t,np.squeeze(t2m['data']),label='2米温度')
    ax.plot(t2m_t, np.squeeze(Td2m), dashes=[6, 2],linewidth=4,c='#00796B',label='2米露点温度')
    ax.plot(t2m_t, np.squeeze(AT), dashes=[6, 2],linewidth=3,c='#FF9933',label='2米体感温度')
    ax.tick_params(length=10)
    ax.grid()
    ax.grid(axis='x',c='black')
    miloc = mpl.dates.HourLocator(byhour=(11,14,17,23,2,5)) #单位是小时
    ax.xaxis.set_minor_locator(miloc)
    ymajorLocator   = MultipleLocator(5) #将此y轴次刻度标签设置为5的倍数
    ax.yaxis.set_major_locator(ymajorLocator)    
    ax.grid(axis='x', which='minor')
    plt.xlim(time_all[0],time_all[-1])
    plt.ylim(min([np.array(Td2m).min(),AT.values.min(),t2m['data'].values.min()])-3,
        math.floor(max([np.array(Td2m).max(),AT.values.max(),t2m['data'].values.max()])/5.)*5+10)
    ax.legend(fontsize=10,loc='upper right')
    ax.set_ylabel('2米温度 体感温度\n'+'2米露点温度 ($^\circ$C)', fontsize=15)
    
                      
    #10米风——————————————————————————————————————
    ax = plt.axes([0.05,0.66,.94,.15])
    for ifhour in u10m['forecast_period'].values:
        if (ifhour == u10m['forecast_period'].values[0] ):
            uv10m_t=(initTime1
                +timedelta(hours=ifhour))
        else:
            uv10m_t=np.append(uv10m_t,
                            (initTime1
                            +timedelta(hours=ifhour)))

    for ifhour in u100m['forecast_period'].values:
        if (ifhour == u100m['forecast_period'].values[0] ):
            uv100m_t=(initTime1
                +timedelta(hours=ifhour))
        else:
            uv100m_t=np.append(uv100m_t,
                            (initTime1
                            +timedelta(hours=ifhour)))
            
    for ifhour in gust10m['forecast_period'].values:
        if (ifhour == gust10m['forecast_period'].values[0] ):
            gust10m_t=(initTime1
                +timedelta(hours=ifhour))
        else:
            gust10m_t=np.append(gust10m_t,
                            (initTime1
                            +timedelta(hours=ifhour)))

    ax.plot(uv10m_t, np.squeeze(wsp10m), c='#40C4FF',label='10米风',linewidth=3)
    ax.plot(uv100m_t,np.squeeze(wsp100m),c='#FF6F00',label='100米风',linewidth=3)
    ax.plot(gust10m_t,np.squeeze(gust10m['data']),c='#7C4DFF',label='10米阵风',linewidth=3)
    if(drw_thr == True):
        ax.plot([uv10m_t[0],uv10m_t[-1]],[5.5,5.5],c='#4CAE50',label='10米平均风一般影响',linewidth=1)
        ax.plot([uv10m_t[0],uv10m_t[-1]],[8,8],c='#FFEB3B',label='10米平均风较大影响',linewidth=1)
        ax.plot([uv10m_t[0],uv10m_t[-1]],[10.8,10.8],c='#F44336',label='10米平均风高影响',linewidth=1)

        ax.plot([gust10m_t[0],gust10m_t[-1]],[10.8,10.8],c='#4CAE50',label='10米阵风一般影响', dashes=[6, 2],linewidth=1)
        ax.plot([gust10m_t[0],gust10m_t[-1]],[13.9,13.9],c='#FFEB3B',label='10米阵风较大影响', dashes=[6, 2],linewidth=1)
        ax.plot([gust10m_t[0],gust10m_t[-1]],[17.2,17.2],c='#F44336',label='10米阵风高影响', dashes=[6, 2],linewidth=1)

    ax.barbs(uv10m_t[0:-1], wsp10m[0:-1], 
            np.squeeze(u10m['data'])[0:-1], np.squeeze(v10m['data'])[0:-1],
            fill_empty=True,color='gray',barb_increments={'half':2,'full':4,'flag':20})

    ax.barbs(uv100m_t[0:-1], wsp100m[0:-1], 
            np.squeeze(u100m['data'])[0:-1], np.squeeze(v100m['data'])[0:-1],
            fill_empty=True,color='gray',barb_increments={'half':2,'full':4,'flag':20})

    xaxis_intaval=mpl.dates.HourLocator(byhour=(8,20)) #单位是小时
    ax.xaxis.set_major_locator(xaxis_intaval)
    ax.set_xticklabels([' '])
    plt.xlim(time_all[0],time_all[-1])    
    # add legend
    ax.legend(fontsize=10,loc='upper right')
    ax.tick_params(length=10)    
    ax.grid()
    ax.grid(axis='x',c='black')
    miloc = mpl.dates.HourLocator(byhour=(11,14,17,23,2,5)) #单位是小时
    ax.xaxis.set_minor_locator(miloc)
    ax.grid(axis='x', which='minor')    
    ax.set_ylabel('10米风 100米 风\n'+'风速 (m/s)', fontsize=15)
    #降水——————————————————————————————————————
    # draw main figure
    ax = plt.axes([0.05,0.49,.94,.15])
    for ifhour in r03['forecast_period'].values:
        if (ifhour == r03['forecast_period'].values[0] ):
            r03_t=(initTime1
                +timedelta(hours=ifhour))
        else:
            r03_t=np.append(r03_t,
                            (initTime1
                            +timedelta(hours=ifhour)))
    #开启自适应
    xaxis_intaval=mpl.dates.HourLocator(byhour=(8,20)) #单位是小时
    ax.xaxis.set_major_locator(xaxis_intaval)
    ax.set_xticklabels([' '])
    ax.bar(r03_t,np.squeeze(r03['data']),width=0.12,color='#1E88E5')
    gap_hour_r03=int(r03['forecast_period'].values[1]-r03['forecast_period'].values[0])

    if(drw_thr == True):
        ax.plot([r03_t[0],r03_t[-1]],[1*gap_hour_r03,1*gap_hour_r03],c='#FFEB3B',label=str(gap_hour_r03)+'小时降水较大影响',linewidth=1)
        ax.plot([r03_t[0],r03_t[-1]],[10*gap_hour_r03,10*gap_hour_r03],c='#F44336',label=str(gap_hour_r03)+'小时降水高影响',linewidth=1)
        ax.legend(fontsize=10,loc='upper right')
    ax.tick_params(length=10)    
    ax.grid()
    ax.grid(axis='x',c='black')
    miloc = mpl.dates.HourLocator(byhour=(11,14,17,23,2,5)) #单位是小时
    ax.xaxis.set_minor_locator(miloc)
    ax.grid(axis='x', which='minor')    
    plt.xlim(time_all[0],time_all[-1])
    plt.ylim([np.squeeze(r03['data']).values.min(),np.squeeze(r03['data'].values.max())+2])
    ax.set_ylabel(str(gap_hour_r03)+'小时累积雨量 (mm)', fontsize=15)
    #总量云——————————————————————————————————————
    # draw main figure
    ax = plt.axes([0.05,0.32,.94,.15])
    for ifhour in TCDC['forecast_period'].values:
        if (ifhour == TCDC['forecast_period'].values[0] ):
            TCDC_t=(initTime1
                +timedelta(hours=ifhour))
        else:
            TCDC_t=np.append(TCDC_t,
                            (initTime1
                            +timedelta(hours=ifhour)))
    # draw main figure
    for ifhour in LCDC['forecast_period'].values:
        if (ifhour == LCDC['forecast_period'].values[0] ):
            LCDC_t=(initTime1
                +timedelta(hours=ifhour))
        else:
            LCDC_t=np.append(LCDC_t,
                            (initTime1
                            +timedelta(hours=ifhour)))

    #开启自适应
    xaxis_intaval=mpl.dates.HourLocator(byhour=(8,20)) #单位是小时
    ax.xaxis.set_major_locator(xaxis_intaval)
    ax.set_xticklabels([' '])

    ax.bar(TCDC_t,np.squeeze(TCDC['data']),width=0.20,color='#82B1FF',label='总云量')
    ax.bar(LCDC_t,np.squeeze(LCDC['data']),width=0.125,color='#2962FF',label='低云量')
    ax.tick_params(length=10)    
    ax.grid()
    ax.grid(axis='x',c='black')
    miloc = mpl.dates.HourLocator(byhour=(11,14,17,23,2,5)) #单位是小时
    ax.xaxis.set_minor_locator(miloc)
    ax.grid(axis='x', which='minor')    
    plt.xlim(time_all[0],time_all[-1])
    plt.ylim(0,100)
    ax.legend(fontsize=10,loc='upper right')
    ax.set_ylabel('云量 (%)', fontsize=15)

    if(draw_VIS==False):
        xstklbls = mpl.dates.DateFormatter('%m月%d日%H时')
        ax.xaxis.set_major_formatter(xstklbls)
        for label in ax.get_xticklabels():
            label.set_rotation(30)
            label.set_horizontalalignment('center')
        
        #发布信息————————————————————————————————————————————————
        ax = plt.axes([0.05,0.08,.94,.05])
        ax.axis([0, 10, 0, 10])
        ax.axis('off')
        utl.add_logo_extra_in_axes(pos=[0.7,0.23,.05,.05],which='nmc', size='Xlarge')
        ax.text(7.5, 33,(initTime1 - timedelta(hours=2)).strftime("%Y年%m月%d日%H时")+'发布',size=15)

    if(draw_VIS==True):
        #能见度——————————————————————————————————————
        # draw main figure
        ax = plt.axes([0.05,0.15,.94,.15])

        #VIS=pd.read_csv(dir_all['VIS_SC']+last_file[model])
        for ifhour in VIS['forecast_period'].values:
            if (ifhour == VIS['forecast_period'].values[0] ):
                VIS_t=(initTime2
                    +timedelta(hours=ifhour))
            else:
                VIS_t=np.append(VIS_t,
                                (initTime2
                                +timedelta(hours=ifhour)))

        #开启自适应
        xaxis_intaval=mpl.dates.HourLocator(byhour=(8,20)) #单位是小时
        ax.xaxis.set_major_locator(xaxis_intaval)

        ax.fill_between(VIS_t, np.squeeze(VIS['data']), -100,facecolor='#B3E5FC')
        ax.fill_between(VIS_t, np.squeeze(VIS['data']), 1,facecolor='#81D4FA')
        ax.fill_between(VIS_t, np.squeeze(VIS['data']), 3,facecolor='#4FC3F7')
        ax.fill_between(VIS_t, np.squeeze(VIS['data']), 5,facecolor='#29B6F6')
        ax.fill_between(VIS_t, np.squeeze(VIS['data']), 10,facecolor='#03A9F4')
        ax.fill_between(VIS_t, np.squeeze(VIS['data']), 15,facecolor='#039BE5')
        ax.fill_between(VIS_t, np.squeeze(VIS['data']), 20,facecolor='#0288D1')
        ax.fill_between(VIS_t, np.squeeze(VIS['data']), 25,facecolor='#0277BD')
        ax.fill_between(VIS_t, np.squeeze(VIS['data']), 30,facecolor='#01579B')
        ax.fill_between(VIS_t, np.squeeze(VIS['data']), 100,facecolor='#FFFFFF')

        ax.plot(VIS_t,np.squeeze(VIS['data']))
        if(drw_thr == True):
            ax.plot([VIS_t[0],VIS_t[-1]],[5,5],c='#4CAF50',label='能见度一般影响',linewidth=1)
            ax.plot([VIS_t[0],VIS_t[-1]],[3,3],c='#FFEB3B',label='能见度较大影响',linewidth=1)
            ax.plot([VIS_t[0],VIS_t[-1]],[1,1],c='#F44336',label='能见度高影响',linewidth=1)
            ax.legend(fontsize=10,loc='upper right')

        xstklbls = mpl.dates.DateFormatter('%m月%d日%H时')
        ax.xaxis.set_major_formatter(xstklbls)
        for label in ax.get_xticklabels():
            label.set_rotation(30)
            label.set_horizontalalignment('center')
        ax.tick_params(length=10)
        ax.grid()
        ax.grid(axis='x',c='black')
        miloc = mpl.dates.HourLocator(byhour=(11,14,17,23,2,5)) #单位是小时
        ax.xaxis.set_minor_locator(miloc)
        ax.grid(axis='x', which='minor')    
        plt.xlim(time_all[0],time_all[-1])
        plt.ylim(0,25)
        ax.set_ylabel('能见度 （km）', fontsize=15)
            #发布信息————————————————————————————————————————————————
        ax = plt.axes([0.05,0.08,.94,.05])
        ax.axis([0, 10, 0, 10])
        ax.axis('off')
        utl.add_logo_extra_in_axes(pos=[0.7,0.06,.05,.05],which='nmc', size='Xlarge')
        ax.text(7.5, 0.1,
                (initTime2 - timedelta(hours=2)).strftime("%Y年%m月%d日%H时")+'发布',size=15)

    #出图——————————————————————————————————————————————————————————
    if(output_dir != None ):
        isExists=os.path.exists(output_dir)
        if not isExists:
            os.makedirs(output_dir)
        plt.savefig(output_dir+extra_info['output_head_name']+
        initTime1.strftime("%Y%m%d%H")+
        '00'+extra_info['output_tail_name']+'.jpg', dpi=200,bbox_inches='tight')
    else:
        plt.show()


def draw_Station_Snow_Synthetical_Forecast_From_Cassandra(
            TWC=None,AT=None,u10m=None,v10m=None,u100m=None,v100m=None,
            gust10m=None,wsp10m=None,wsp100m=None,SNOD1=None,SNOD2=None,SDEN=None,SN06=None,
            draw_VIS=False,VIS=None,drw_thr=False,
            time_all=None,
            model=None,points=None,
            output_dir=None,extra_info={
            'output_head_name':' ',
            'output_tail_name':' ',
            'point_name':' '}):

    #if(sys.platform[0:3] == 'win'):
    plt.rcParams['font.sans-serif'] = ['SimHei'] # 步骤一（替换sans-serif字体）
    plt.rcParams['axes.unicode_minus'] = False  # 步骤二（解决坐标轴负数的负号显示问题）
    if(sys.platform[0:3] == 'lin'):
        locale.setlocale(locale.LC_CTYPE, 'zh_CN.utf8')
    if(sys.platform[0:3] == 'win'):        
        locale.setlocale(locale.LC_CTYPE, 'chinese')       

    initTime1=pd.to_datetime(str(TWC['forecast_reference_time'].values)).replace(tzinfo=None).to_pydatetime()
    initTime2=pd.to_datetime(str(VIS['forecast_reference_time'].values)).replace(tzinfo=None).to_pydatetime()

    # draw figure
    fig=plt.figure(figsize=(12,16))
    # draw main figure
    #风寒指数 体感温度————————————————————————————————————————————————
    ax = plt.axes([0.05,0.83,.94,.15])
    utl.add_public_title_sta(title=model+'预报 '+extra_info['point_name']+' ['+str(points['lon'][0])+','+str(points['lat'][0])+']',initTime=initTime1, fontsize=23)

    for ifhour in TWC['forecast_period'].values:
        if (ifhour == TWC['forecast_period'].values[0] ):
            TWC_t=(initTime1
                +timedelta(hours=ifhour))
        else:
            TWC_t=np.append(TWC_t,
                            (initTime1
                            +timedelta(hours=ifhour)))
    #开启自适应
    xaxis_intaval=mpl.dates.HourLocator(byhour=(8,20)) #单位是小时
    ax.xaxis.set_major_locator(xaxis_intaval)
    ax.set_xticklabels([' '])
    ax.plot(TWC_t,np.squeeze(TWC),label='风寒指数')
    ax.plot(TWC_t, np.squeeze(AT), c='#00796B',label='2米体感温度')
    ax.tick_params(length=10)
    ax.grid()
    ax.grid(axis='x',c='black')
    miloc = mpl.dates.HourLocator(byhour=(11,14,17,23,2,5)) #单位是小时
    ax.xaxis.set_minor_locator(miloc)
    ax.grid(axis='x', which='minor')
    plt.xlim(time_all[0],time_all[-1])
    plt.ylim(min([AT.values.min(),TWC.values.min()]),
        max([AT.values.max(),TWC.values.max()]))
    ax.legend(fontsize=10,loc='upper right')
    ax.set_ylabel('2米体感温度 风寒指数 ($^\circ$C)', fontsize=15)
    
                      
    #10米风——————————————————————————————————————
    ax = plt.axes([0.05,0.66,.94,.15])
    for ifhour in u10m['forecast_period'].values:
        if (ifhour == u10m['forecast_period'].values[0] ):
            uv10m_t=(initTime1
                +timedelta(hours=ifhour))
        else:
            uv10m_t=np.append(uv10m_t,
                            (initTime1
                            +timedelta(hours=ifhour)))

    for ifhour in u100m['forecast_period'].values:
        if (ifhour == u100m['forecast_period'].values[0] ):
            uv100m_t=(initTime1
                +timedelta(hours=ifhour))
        else:
            uv100m_t=np.append(uv100m_t,
                            (initTime1
                            +timedelta(hours=ifhour)))
            
    for ifhour in gust10m['forecast_period'].values:
        if (ifhour == gust10m['forecast_period'].values[0] ):
            gust10m_t=(initTime1
                +timedelta(hours=ifhour))
        else:
            gust10m_t=np.append(gust10m_t,
                            (initTime1
                            +timedelta(hours=ifhour)))

    ax.plot(uv10m_t, np.squeeze(wsp10m), c='#40C4FF',label='10米风',linewidth=3)
    ax.plot(uv100m_t,np.squeeze(wsp100m),c='#FF6F00',label='100米风',linewidth=3)
    ax.plot(gust10m_t,np.squeeze(gust10m['data']),c='#7C4DFF',label='10米阵风',linewidth=3)
    if(drw_thr == True):
        ax.plot([uv10m_t[0],uv10m_t[-1]],[5.5,5.5],c='#4CAE50',label='10米平均风一般影响',linewidth=1)
        ax.plot([uv10m_t[0],uv10m_t[-1]],[8,8],c='#FFEB3B',label='10米平均风较大影响',linewidth=1)
        ax.plot([uv10m_t[0],uv10m_t[-1]],[10.8,10.8],c='#F44336',label='10米平均风高影响',linewidth=1)

        ax.plot([gust10m_t[0],gust10m_t[-1]],[10.8,10.8],c='#4CAE50',label='10米阵风一般影响', dashes=[6, 2],linewidth=1)
        ax.plot([gust10m_t[0],gust10m_t[-1]],[13.9,13.9],c='#FFEB3B',label='10米阵风较大影响', dashes=[6, 2],linewidth=1)
        ax.plot([gust10m_t[0],gust10m_t[-1]],[17.2,17.2],c='#F44336',label='10米阵风高影响', dashes=[6, 2],linewidth=1)

    ax.barbs(uv10m_t[0:-1], wsp10m[0:-1], 
            np.squeeze(u10m['data'])[0:-1], np.squeeze(v10m['data'])[0:-1],
            fill_empty=True,color='gray',barb_increments={'half':2,'full':4,'flag':20})

    ax.barbs(uv100m_t[0:-1], wsp100m[0:-1], 
            np.squeeze(u100m['data'])[0:-1], np.squeeze(v100m['data'])[0:-1],
            fill_empty=True,color='gray',barb_increments={'half':2,'full':4,'flag':20})

    xaxis_intaval=mpl.dates.HourLocator(byhour=(8,20)) #单位是小时
    ax.xaxis.set_major_locator(xaxis_intaval)
    ax.set_xticklabels([' '])
    plt.xlim(time_all[0],time_all[-1])    
    # add legend
    ax.legend(fontsize=10,loc='upper right')
    ax.tick_params(length=10)    
    ax.grid()
    ax.grid(axis='x',c='black')
    miloc = mpl.dates.HourLocator(byhour=(11,14,17,23,2,5)) #单位是小时
    ax.xaxis.set_minor_locator(miloc)
    ax.grid(axis='x', which='minor')    
    ax.set_ylabel('10米风 100米 风\n'+'风速 (m/s)', fontsize=15)
    #雪密度——————————————————————————————————————
    # draw main figure
    ax = plt.axes([0.05,0.49,.94,.15])
    for ifhour in SDEN['forecast_period'].values:
        if (ifhour == SDEN['forecast_period'].values[0] ):
            SDEN_t=(initTime1
                +timedelta(hours=ifhour))
        else:
            SDEN_t=np.append(SDEN_t,
                            (initTime1
                            +timedelta(hours=ifhour)))
    #开启自适应
    xaxis_intaval=mpl.dates.HourLocator(byhour=(8,20)) #单位是小时
    ax.xaxis.set_major_locator(xaxis_intaval)
    ax.set_xticklabels([' '])

    ax.plot(SDEN_t,np.squeeze(SDEN['data']),color='#1E88E5',label='雪密度')
    #ax.bar(SDEN_t,np.squeeze(SDEN['data']),width=0.12,color='#1E88E5')
    gap_hour_SDEN=int(SDEN['forecast_period'].values[1]-SDEN['forecast_period'].values[0])

    if(drw_thr == True):
        ax.plot([SDEN_t[0],SDEN_t[-1]],[1*gap_hour_SDEN,1*gap_hour_SDEN],c='#FFEB3B',label=str(gap_hour_SDEN)+'小时降水较大影响',linewidth=1)
        ax.plot([SDEN_t[0],SDEN_t[-1]],[10*gap_hour_SDEN,10*gap_hour_SDEN],c='#F44336',label=str(gap_hour_SDEN)+'小时降水高影响',linewidth=1)
        ax.legend(fontsize=10,loc='upper right')
    ax.tick_params(length=10)    
    ax.grid()
    ax.grid(axis='x',c='black')
    miloc = mpl.dates.HourLocator(byhour=(11,14,17,23,2,5)) #单位是小时
    ax.xaxis.set_minor_locator(miloc)
    ax.grid(axis='x', which='minor')    
    plt.xlim(time_all[0],time_all[-1])
    plt.ylim([np.squeeze(SDEN['data']).values.min(),np.squeeze(SDEN['data'].values.max())+2])
    ax.set_ylabel('雪密度 (kg m-3)', fontsize=15)
    #积雪深度——————————————————————————————————————
    # draw main figure
    ax = plt.axes([0.05,0.32,.94,.15])
    for ifhour in SNOD1['forecast_period'].values:
        if (ifhour == SNOD1['forecast_period'].values[0] ):
            SNOD1_t=(initTime1
                +timedelta(hours=ifhour))
        else:
            SNOD1_t=np.append(SNOD1_t,
                            (initTime1
                            +timedelta(hours=ifhour)))
    # draw main figure
    for ifhour in SNOD2['forecast_period'].values:
        if (ifhour == SNOD2['forecast_period'].values[0] ):
            SNOD2_t=(initTime1
                +timedelta(hours=ifhour))
        else:
            SNOD2_t=np.append(SNOD2_t,
                            (initTime1
                            +timedelta(hours=ifhour)))

    for ifhour in SN06['forecast_period'].values:
        if (ifhour == SN06['forecast_period'].values[0] ):
            SN06_t=(initTime1
                +timedelta(hours=ifhour))
        else:
            SN06_t=np.append(SN06_t,
                            (initTime1
                            +timedelta(hours=ifhour)))
    #开启自适应
    xaxis_intaval=mpl.dates.HourLocator(byhour=(8,20)) #单位是小时
    ax.xaxis.set_major_locator(xaxis_intaval)
    ax.set_xticklabels([' '])

    #ax.bar(SNOD1_t,np.squeeze(SNOD1['data']),width=0.20,color='#82B1FF',label='EC预报积雪深度')
    #ax.bar(SNOD2_t,np.squeeze(SNOD2['data']),width=0.125,color='#2962FF',label='NCEP预报积雪深度')
    ax.plot(SNOD1_t,np.squeeze(SNOD1['data']), dashes=[6, 2],color='#4B4B4B',linewidth=3,label='EC预报积雪深度')
    ax.plot(SNOD2_t,np.squeeze(SNOD2['data']), dashes=[6, 2],color='#969696',linewidth=3,label='NCEP预报积雪深度')
    ax.plot(SN06_t,np.squeeze(SN06['data']),color='#82B1FF',linewidth=2,label='EC预报降雪量')

    ax.tick_params(length=10)    
    ax.grid()
    ax.grid(axis='x',c='black')
    miloc = mpl.dates.HourLocator(byhour=(11,14,17,23,2,5)) #单位是小时
    ax.xaxis.set_minor_locator(miloc)
    ax.grid(axis='x', which='minor')    
    plt.xlim(time_all[0],time_all[-1])
    plt.ylim(0,100)
    ax.legend(fontsize=10,loc='upper right')
    plt.ylim(min([np.squeeze(SNOD1['data']).values.min(),np.squeeze(SNOD2['data']).values.min()]),
        max([np.squeeze(SNOD1['data']).values.max(),np.squeeze(SNOD2['data']).values.max()])+5)
    ax.set_ylabel('积雪深度 (cm)\n'+'6小时降雪量(mm)', fontsize=15)

    if(draw_VIS==False):
        xstklbls = mpl.dates.DateFormatter('%m月%d日%H时')
        ax.xaxis.set_major_formatter(xstklbls)
        for label in ax.get_xticklabels():
            label.set_rotation(30)
            label.set_horizontalalignment('center')
        
        #发布信息————————————————————————————————————————————————
        ax = plt.axes([0.05,0.08,.94,.05])
        ax.axis([0, 10, 0, 10])
        ax.axis('off')
        utl.add_logo_extra_in_axes(pos=[0.7,0.23,.05,.05],which='nmc', size='Xlarge')
        ax.text(7.5, 33,(initTime1 - timedelta(hours=2)).strftime("%Y年%m月%d日%H时")+'发布',size=15)

    if(draw_VIS==True):
        #能见度——————————————————————————————————————
        # draw main figure
        ax = plt.axes([0.05,0.15,.94,.15])

        #VIS=pd.read_csv(dir_all['VIS_SC']+last_file[model])
        for ifhour in VIS['forecast_period'].values:
            if (ifhour == VIS['forecast_period'].values[0] ):
                VIS_t=(initTime2
                    +timedelta(hours=ifhour))
            else:
                VIS_t=np.append(VIS_t,
                                (initTime2
                                +timedelta(hours=ifhour)))

        #开启自适应
        xaxis_intaval=mpl.dates.HourLocator(byhour=(8,20)) #单位是小时
        ax.xaxis.set_major_locator(xaxis_intaval)

        ax.fill_between(VIS_t, np.squeeze(VIS['data']), -100,facecolor='#B3E5FC')
        ax.fill_between(VIS_t, np.squeeze(VIS['data']), 1,facecolor='#81D4FA')
        ax.fill_between(VIS_t, np.squeeze(VIS['data']), 3,facecolor='#4FC3F7')
        ax.fill_between(VIS_t, np.squeeze(VIS['data']), 5,facecolor='#29B6F6')
        ax.fill_between(VIS_t, np.squeeze(VIS['data']), 10,facecolor='#03A9F4')
        ax.fill_between(VIS_t, np.squeeze(VIS['data']), 15,facecolor='#039BE5')
        ax.fill_between(VIS_t, np.squeeze(VIS['data']), 20,facecolor='#0288D1')
        ax.fill_between(VIS_t, np.squeeze(VIS['data']), 25,facecolor='#0277BD')
        ax.fill_between(VIS_t, np.squeeze(VIS['data']), 30,facecolor='#01579B')
        ax.fill_between(VIS_t, np.squeeze(VIS['data']), 100,facecolor='#FFFFFF')

        ax.plot(VIS_t,np.squeeze(VIS['data']))
        if(drw_thr == True):
            ax.plot([VIS_t[0],VIS_t[-1]],[5,5],c='#4CAF50',label='能见度一般影响',linewidth=1)
            ax.plot([VIS_t[0],VIS_t[-1]],[3,3],c='#FFEB3B',label='能见度较大影响',linewidth=1)
            ax.plot([VIS_t[0],VIS_t[-1]],[1,1],c='#F44336',label='能见度高影响',linewidth=1)
            ax.legend(fontsize=10,loc='upper right')

        xstklbls = mpl.dates.DateFormatter('%m月%d日%H时')
        ax.xaxis.set_major_formatter(xstklbls)
        for label in ax.get_xticklabels():
            label.set_rotation(30)
            label.set_horizontalalignment('center')
        ax.tick_params(length=10)
        ax.grid()
        ax.grid(axis='x',c='black')
        miloc = mpl.dates.HourLocator(byhour=(11,14,17,23,2,5)) #单位是小时
        ax.xaxis.set_minor_locator(miloc)
        ax.grid(axis='x', which='minor')    
        plt.xlim(time_all[0],time_all[-1])
        plt.ylim(0,25)
        ax.set_ylabel('能见度 （km）', fontsize=15)
            #发布信息————————————————————————————————————————————————
        ax = plt.axes([0.05,0.08,.94,.05])
        ax.axis([0, 10, 0, 10])
        ax.axis('off')
        utl.add_logo_extra_in_axes(pos=[0.7,0.06,.05,.05],which='nmc', size='Xlarge')
        ax.text(7.5, 0.1,
                (initTime2 - timedelta(hours=2)).strftime("%Y年%m月%d日%H时")+'发布',size=15)

    #出图——————————————————————————————————————————————————————————
    if(output_dir != None ):
        isExists=os.path.exists(output_dir)
        if not isExists:
            os.makedirs(output_dir)
        plt.savefig(output_dir+extra_info['output_head_name']+
        initTime1.strftime("%Y%m%d%H")+
        '00'+extra_info['output_tail_name']+'.jpg', dpi=200,bbox_inches='tight')
    else:
        plt.show()


def draw_sta_skewT(p=None,T=None,Td=None,wind_speed=None,wind_dir=None,u=None,v=None,
    fcst_info=None,output_dir=None):
    fig = plt.figure(figsize=(9, 9))
    skew = SkewT(fig, rotation=45)

    plt.rcParams['font.sans-serif'] = ['SimHei'] # 步骤一（替换sans-serif字体）
    plt.rcParams['axes.unicode_minus'] = False  # 步骤二（解决坐标轴负数的负号显示问题）

    # Plot the data using normal plotting functions, in this case using
    # log scaling in Y, as dictated by the typical meteorological plot.
    skew.plot(p, T, 'r')
    skew.plot(p, Td, 'g')
    skew.plot_barbs(p, u, v)
    skew.ax.set_ylim(1000, 100)
    skew.ax.set_xlim(-40, 60)

    # Calculate LCL height and plot as black dot. Because `p`'s first value is
    # ~1000 mb and its last value is ~250 mb, the `0` index is selected for
    # `p`, `T`, and `Td` to lift the parcel from the surface. If `p` was inverted,
    # i.e. start from low value, 250 mb, to a high value, 1000 mb, the `-1` index
    # should be selected.
    lcl_pressure, lcl_temperature = mpcalc.lcl(p[0], T[0], Td[0])
    skew.plot(lcl_pressure, lcl_temperature, 'ko', markerfacecolor='black')

    # Calculate full parcel profile and add to plot as black line
    prof = mpcalc.parcel_profile(p, T[0], Td[0]).to('degC')
    skew.plot(p, prof, 'k', linewidth=2)

    # Shade areas of CAPE and CIN
    skew.shade_cin(p, T, prof)
    skew.shade_cape(p, T, prof)

    # An example of a slanted line at constant T -- in this case the 0
    # isotherm
    skew.ax.axvline(0, color='c', linestyle='--', linewidth=2)

    # Add the relevant special lines
    skew.plot_dry_adiabats()
    skew.plot_moist_adiabats()
    skew.plot_mixing_lines()

    #forecast information
    bax=plt.axes([0.12,0.88,.25,.07],facecolor='#FFFFFFCC')
    bax.axis('off')
    bax.axis([0, 10, 0, 10])

    initTime = pd.to_datetime(
        str(fcst_info['forecast_reference_time'].values)).replace(tzinfo=None).to_pydatetime()
    if(sys.platform[0:3] == 'lin'):
        locale.setlocale(locale.LC_CTYPE, 'zh_CN.utf8')
    if(sys.platform[0:3] == 'win'):        
        locale.setlocale(locale.LC_CTYPE, 'chinese')
    plt.text(2.5, 7.5,'起报时间: '+initTime.strftime("%Y年%m月%d日%H时"),size=11)
    plt.text(2.5, 5.0,'['+str(fcst_info.attrs['model'])+'] '+str(int(fcst_info['forecast_period'].values[0]))+'小时预报探空',size=11)
    plt.text(2.5, 2.5,'预报点: '+str(fcst_info.attrs['points']['lon'])+
        ', '+str(fcst_info.attrs['points']['lat']),size=11)
    plt.text(2.5, 0.5,'www.nmc.cn',size=11)
    utl.add_logo_extra_in_axes(pos=[0.1,0.88,.07,.07],which='nmc', size='Xlarge')

    # Show the plot
    if(output_dir != None ):
        plt.savefig(output_dir+'时间剖面产品_起报时间_'+
        str(fcst_info['forecast_reference_time'].values)[0:13]+
        '_预报时效_'+str(int(fcst_info.attrs['forecast_period'].values))
        +'.png', dpi=200,bbox_inches='tight')
    else:
        plt.show()

def draw_point_wind(U=None,V=None,
        model=None,
        output_dir=None,
        points=None,
        time_info=None,
        extra_info=None):

    plt.rcParams['font.sans-serif'] = ['SimHei'] # 步骤一（替换sans-serif字体）
    plt.rcParams['axes.unicode_minus'] = False  # 步骤二（解决坐标轴负数的负号显示问题）
    if(sys.platform[0:3] == 'lin'):
        locale.setlocale(locale.LC_CTYPE, 'zh_CN.utf8')
    if(sys.platform[0:3] == 'win'):        
        locale.setlocale(locale.LC_CTYPE, 'chinese')       

    initTime=pd.to_datetime(str(time_info['forecast_reference_time'].values)).replace(tzinfo=None).to_pydatetime()

    # draw figure
    fig=plt.figure(figsize=(12,12))
    # draw main figure    
    #10米风——————————————————————————————————————
    ax = plt.axes([0.1,0.2,.8,.7])
    utl.add_public_title_sta(title=model+'预报 '+extra_info['point_name']+' ['+str(points['lon'][0])+','+str(points['lat'][0])+']',initTime=initTime, fontsize=21)
    for ifhour in time_info['forecast_period'].values:
        if (ifhour == time_info['forecast_period'].values[0] ):
            uv_t=(initTime
                +timedelta(hours=ifhour))
        else:
            uv_t=np.append(uv_t,
                            (initTime
                            +timedelta(hours=ifhour)))

    wsp=(U**2+V**2)**0.5
    ax.plot(uv_t, np.squeeze(wsp), c='#40C4FF',linewidth=3)
    if(extra_info['drw_thr'] == True):
        ax.plot([uv_t[0],uv_t[-1]],[11,11],c='red',label='警戒风速',linewidth=1)

    ax.barbs(uv_t, wsp,U,V,
            fill_empty=True,color='gray',barb_increments={'half':2,'full':4,'flag':20})

    xaxis_intaval=mpl.dates.HourLocator(byhour=(8,20)) #单位是小时
    ax.xaxis.set_major_locator(xaxis_intaval)
    plt.xlim(uv_t[0],uv_t[-1])    
    # add legend
    ax.legend(fontsize=15,loc='upper right')
    ax.tick_params(length=10)   
    xstklbls = mpl.dates.DateFormatter('%m月%d日%H时')
    for label in ax.get_xticklabels():
        label.set_rotation(30)
        label.set_horizontalalignment('center')
    ax.tick_params(axis='y',labelsize=15)
    ax.tick_params(axis='x',labelsize=15)

    ax.grid()
    ax.grid(axis='x',c='black')
    miloc = mpl.dates.HourLocator(byhour=(11,14,17,23,2,5)) #单位是小时
    ax.xaxis.set_minor_locator(miloc)
    ax.grid(axis='x', which='minor')    
    ax.set_ylabel('风速 (m/s)', fontsize=15)

    utl.add_logo_extra_in_axes(pos=[0.1,0.8,.1,.1],which='nmc', size='Xlarge')

    #出图——————————————————————————————————————————————————————————
    if(output_dir != None ):
        isExists=os.path.exists(output_dir)
        if not isExists:
            os.makedirs(output_dir)

        output_dir2=output_dir+model+'_起报时间_'+initTime.strftime("%Y年%m月%d日%H时")+'/'
        if(os.path.exists(output_dir2) == False):
            os.makedirs(output_dir2)

        plt.savefig(output_dir2+model+'_'+extra_info['point_name']+'_'+extra_info['output_head_name']+
        initTime.strftime("%Y%m%d%H")+
        '00'+extra_info['output_tail_name']+'.jpg', dpi=200,bbox_inches='tight')
    else:
        plt.show()


def draw_point_fcst(t2m=None,u10m=None,v10m=None,rn=None,
        model=None,
        output_dir=None,
        points=None,
        extra_info=None):

    plt.rcParams['font.sans-serif'] = ['SimHei'] # 步骤一（替换sans-serif字体）
    plt.rcParams['axes.unicode_minus'] = False  # 步骤二（解决坐标轴负数的负号显示问题）
    if(sys.platform[0:3] == 'lin'):
        locale.setlocale(locale.LC_CTYPE, 'zh_CN.utf8')
    if(sys.platform[0:3] == 'win'):        
        locale.setlocale(locale.LC_CTYPE, 'chinese')       

    initTime=pd.to_datetime(str(t2m['forecast_reference_time'].values)).replace(tzinfo=None).to_pydatetime()

    # draw figure
    fig=plt.figure(figsize=(16,4.5))
    ax_t2m = HostAxes(fig,[0.1,0.28,.8,.62])
    ax_rn = ParasiteAxes(ax_t2m, sharex=ax_t2m)
    #其他信息


    #append axes
    ax_t2m.parasites.append(ax_rn)

    #invisible right axis of ax
    ax_t2m.axis['right'].set_visible(False)
    ax_t2m.axis['right'].set_visible(False)
    ax_rn.axis['right'].set_visible(True)
    ax_rn.axis['right'].major_ticklabels.set_visible(True)
    ax_rn.axis['right'].label.set_visible(True)
    #set label for axis
    ax_t2m.set_ylabel('温度($^\circ$C)', fontsize=100)
    ax_rn.set_ylabel('降水(mm)', fontsize=100)
    fig.add_axes(ax_t2m)

    # draw main figure    
    #2米温度——————————————————————————————————————
    if(model == '中央台指导'):
        model='智能网格'
    utl.add_public_title_sta(title=model+'预报 '+extra_info['point_name']+' ['+str(points['lon'][0])+','+str(points['lat'][0])+']',initTime=initTime, fontsize=21)
    for ifhour in t2m['forecast_period'].values:
        if (ifhour == t2m['forecast_period'].values[0] ):
            t2m_t=(initTime
                +timedelta(hours=ifhour))
        else:
            t2m_t=np.append(t2m_t,
                            (initTime
                            +timedelta(hours=ifhour)))

    curve_t2m=ax_t2m.plot(t2m_t, np.squeeze(t2m['data'].values), c='#FF6600',linewidth=3,label='2m温度')
    ax_t2m.set_xlim(t2m_t[0],t2m_t[-1])
    ax_t2m.set_ylim(math.floor(t2m['data'].values.min()/5)*5-2,
        math.ceil(t2m['data'].values.max()/5)*5)
    #降水——————————————————————————————————————
    for ifhour in rn['forecast_period'].values:
        if (ifhour == rn['forecast_period'].values[0] ):
            rn_t=(initTime
                +timedelta(hours=ifhour))
        else:
            rn_t=np.append(rn_t,
                            (initTime
                            +timedelta(hours=ifhour)))
    mask = (rn['data'] < 999)
    rn=rn['data'].where(mask)
    ax_rn.bar(rn_t,np.squeeze(rn.values),width=0.1,color='#00008B',
        label=str(int(rn['forecast_period'].values[1]-rn['forecast_period'].values[0]))+'小时降水',alpha=0.5)
    #curve_rn=ax_rn.plot(rn_t, np.squeeze(rn['data'].values), c='#40C4FF',linewidth=3)
    
    ax_rn.set_ylim(0,np.nanmax(np.append(10,np.squeeze(rn.values))))
    ###

    xaxis_intaval=mpl.dates.HourLocator(byhour=(8,20)) #单位是小时
    ax_t2m.xaxis.set_major_locator(xaxis_intaval)
    # add legend
    ax_t2m.legend(fontsize=15,loc='upper right')
    ax_t2m.tick_params(length=10)   
    ax_t2m.tick_params(axis='y',labelsize=100)
    ax_t2m.set_xticklabels([' '])
    miloc = mpl.dates.HourLocator(byhour=(8,11,14,17,20,23,2,5)) #单位是小时
    ax_t2m.xaxis.set_minor_locator(miloc)
    yminorLocator   = MultipleLocator(1) #将此y轴次刻度标签设置为1的倍数
    ax_t2m.yaxis.set_minor_locator(yminorLocator)
    ymajorLocator   = MultipleLocator(5) #将此y轴次刻度标签设置为1的倍数
    ax_t2m.yaxis.set_major_locator(ymajorLocator)

    ax_t2m.grid(axis='x', which='minor',ls='--')    
    ax_t2m.axis['left'].label.set_fontsize(15)
    ax_t2m.axis['left'].major_ticklabels.set_fontsize(15)
    ax_rn.axis['right'].label.set_fontsize(15)
    ax_rn.axis['right'].major_ticklabels.set_fontsize(15)
    #10米风——————————————————————————————————————
    ax_uv = plt.axes([0.1,0.16,.8,.12])
    for ifhour in u10m['forecast_period'].values:
        if (ifhour == u10m['forecast_period'].values[0] ):
            uv_t=(initTime
                +timedelta(hours=ifhour))
        else:
            uv_t=np.append(uv_t,
                            (initTime
                            +timedelta(hours=ifhour)))

    wsp=(u10m**2+v10m**2)**0.5
    #curve_uv=ax_uv.plot(uv_t, np.squeeze(wsp['data'].values), c='#696969',linewidth=3,label='10m风')

    ax_uv.barbs(uv_t, np.zeros(len(uv_t)),
            np.squeeze(u10m['data'].values),np.squeeze(v10m['data'].values),
            fill_empty=True,color='gray',barb_increments={'half':2,'full':4,'flag':20},length=5.8,linewidth=1.5,zorder=100)
    ax_uv.set_ylim(-1,1)
    ax_uv.set_xlim(uv_t[0],uv_t[-1])
    #ax_uv.axis('off')
    ax_uv.set_yticklabels([' '])
    #logo
    utl.add_logo_extra_in_axes(pos=[0.87,0.00,.1,.1],which='nmc', size='Xlarge')

    #开启自适应
    xaxis_intaval=mpl.dates.HourLocator(byhour=(8,20)) #单位是小时
    ax_uv.xaxis.set_major_locator(xaxis_intaval)
    ax_uv.tick_params(length=5,axis='x')
    ax_uv.tick_params(length=0,axis='y')
    miloc = mpl.dates.HourLocator(byhour=(8,11,14,17,20,23,2,5)) #单位是小时
    ax_uv.xaxis.set_minor_locator(miloc)
    ax_uv.grid(axis='x',which='both',ls='--')    
    ax_uv.set_ylabel('10m风', fontsize=15)

    xstklbls = mpl.dates.DateFormatter('%m月%d日%H时')
    for label in ax_uv.get_xticklabels():
        label.set_rotation(30)
        label.set_horizontalalignment('center')
    ax_uv.tick_params(axis='x',labelsize=15)

    #出图——————————————————————————————————————————————————————————
    
    if(output_dir != None ):
        isExists=os.path.exists(output_dir)
        if not isExists:
            os.makedirs(output_dir)

        output_dir2=output_dir+model+'_起报时间_'+initTime.strftime("%Y年%m月%d日%H时")+'/'
        if(os.path.exists(output_dir2) == False):
            os.makedirs(output_dir2)

        plt.savefig(output_dir2+extra_info['point_name']+
        extra_info['output_head_name']+
        initTime.strftime("%Y%m%d%H")+
        '00'+extra_info['output_tail_name']+'.jpg', dpi=200,bbox_inches='tight')
    else:
        plt.show()


def draw_point_uv_rh_fcst(rh2m=None,u10m=None,v10m=None,rn=None,
        model=None,
        output_dir=None,
        points=None,
        extra_info=None):

    plt.rcParams['font.sans-serif'] = ['SimHei'] # 步骤一（替换sans-serif字体）
    plt.rcParams['axes.unicode_minus'] = False  # 步骤二（解决坐标轴负数的负号显示问题）
    if(sys.platform[0:3] == 'lin'):
        locale.setlocale(locale.LC_CTYPE, 'zh_CN.utf8')
    if(sys.platform[0:3] == 'win'):        
        locale.setlocale(locale.LC_CTYPE, 'chinese')       

    initTime=pd.to_datetime(str(rh2m['forecast_reference_time'].values)).replace(tzinfo=None).to_pydatetime()

    # draw figure
    fig=plt.figure(figsize=(16,4.5))
    ax_rh2m = HostAxes(fig,[0.1,0.28,.8,.62])
    ax_rn = ParasiteAxes(ax_rh2m, sharex=ax_rh2m)
    #其他信息


    #append axes
    ax_rh2m.parasites.append(ax_rn)

    #invisible right axis of ax
    ax_rh2m.axis['right'].set_visible(False)
    ax_rh2m.axis['right'].set_visible(False)
    ax_rn.axis['right'].set_visible(True)
    ax_rn.axis['right'].major_ticklabels.set_visible(True)
    ax_rn.axis['right'].label.set_visible(True)
    #set label for axis
    ax_rh2m.set_ylabel('相对湿度(%)', fontsize=100)
    ax_rn.set_ylabel('降水(mm)', fontsize=100)
    fig.add_axes(ax_rh2m)

    # draw main figure    
    #2米温度——————————————————————————————————————
    if(model == '中央台指导'):
        model='智能网格'
    utl.add_public_title_sta(title=model+'预报 '+extra_info['point_name']+' ['+str(points['lon'][0])+','+str(points['lat'][0])+']',initTime=initTime, fontsize=21)
    for ifhour in rh2m['forecast_period'].values:
        if (ifhour == rh2m['forecast_period'].values[0] ):
            rh2m_t=(initTime
                +timedelta(hours=ifhour))
        else:
            rh2m_t=np.append(rh2m_t,
                            (initTime
                            +timedelta(hours=ifhour)))

    curve_t2m=ax_rh2m.plot(rh2m_t, np.squeeze(rh2m['data'].values), c='#FF6600',linewidth=3,label='相对湿度')
    ax_rh2m.set_xlim(rh2m_t[0],rh2m_t[-1])
    ax_rh2m.set_ylim(0,100)
    #降水——————————————————————————————————————
    for ifhour in rn['forecast_period'].values:
        if (ifhour == rn['forecast_period'].values[0] ):
            rn_t=(initTime
                +timedelta(hours=ifhour))
        else:
            rn_t=np.append(rn_t,
                            (initTime
                            +timedelta(hours=ifhour)))
    mask = (rn['data'] < 999)
    rn=rn['data'].where(mask)
    ax_rn.bar(rn_t,np.squeeze(rn.values),width=0.1,color='#00008B',
        label=str(int(rn['forecast_period'].values[1]-rn['forecast_period'].values[0]))+'小时降水',alpha=0.5)
    #curve_rn=ax_rn.plot(rn_t, np.squeeze(rn['data'].values), c='#40C4FF',linewidth=3)
    
    ax_rn.set_ylim(0,np.nanmax(np.append(10,np.squeeze(rn.values))))
    ###

    xaxis_intaval=mpl.dates.HourLocator(byhour=(8,20)) #单位是小时
    ax_rh2m.xaxis.set_major_locator(xaxis_intaval)
    # add legend
    ax_rh2m.legend(fontsize=15,loc='upper right')
    ax_rh2m.tick_params(length=10)   
    ax_rh2m.tick_params(axis='y',labelsize=100)
    ax_rh2m.set_xticklabels([' '])
    miloc = mpl.dates.HourLocator(byhour=(8,11,14,17,20,23,2,5)) #单位是小时
    ax_rh2m.xaxis.set_minor_locator(miloc)
    yminorLocator   = MultipleLocator(10) #将此y轴次刻度标签设置为1的倍数
    ax_rh2m.yaxis.set_minor_locator(yminorLocator)
    ymajorLocator   = MultipleLocator(20) #将此y轴次刻度标签设置为1的倍数
    ax_rh2m.yaxis.set_major_locator(ymajorLocator)

    ax_rh2m.grid(axis='x', which='minor',ls='--')    
    ax_rh2m.axis['left'].label.set_fontsize(15)
    ax_rh2m.axis['left'].major_ticklabels.set_fontsize(15)
    ax_rn.axis['right'].label.set_fontsize(15)
    ax_rn.axis['right'].major_ticklabels.set_fontsize(15)
    #10米风——————————————————————————————————————
    ax_uv = plt.axes([0.1,0.16,.8,.12])
    for ifhour in u10m['forecast_period'].values:
        if (ifhour == u10m['forecast_period'].values[0] ):
            uv_t=(initTime
                +timedelta(hours=ifhour))
        else:
            uv_t=np.append(uv_t,
                            (initTime
                            +timedelta(hours=ifhour)))

    wsp=(u10m**2+v10m**2)**0.5
    #curve_uv=ax_uv.plot(uv_t, np.squeeze(wsp['data'].values), c='#696969',linewidth=3,label='10m风')

    ax_uv.barbs(uv_t, np.zeros(len(uv_t)),
            np.squeeze(u10m['data'].values),np.squeeze(v10m['data'].values),
            fill_empty=True,color='gray',barb_increments={'half':2,'full':4,'flag':20},length=5.8,linewidth=1.5,zorder=100)
    ax_uv.set_ylim(-1,1)
    ax_uv.set_xlim(uv_t[0],uv_t[-1])
    #ax_uv.axis('off')
    ax_uv.set_yticklabels([' '])
    #logo
    utl.add_logo_extra_in_axes(pos=[0.87,0.00,.1,.1],which='nmc', size='Xlarge')

    #开启自适应
    xaxis_intaval=mpl.dates.HourLocator(byhour=(8,20)) #单位是小时
    ax_uv.xaxis.set_major_locator(xaxis_intaval)
    ax_uv.tick_params(length=5,axis='x')
    ax_uv.tick_params(length=0,axis='y')
    miloc = mpl.dates.HourLocator(byhour=(8,11,14,17,20,23,2,5)) #单位是小时
    ax_uv.xaxis.set_minor_locator(miloc)
    ax_uv.grid(axis='x',which='both',ls='--')    
    ax_uv.set_ylabel('10m风', fontsize=15)

    xstklbls = mpl.dates.DateFormatter('%m月%d日%H时')
    for label in ax_uv.get_xticklabels():
        label.set_rotation(30)
        label.set_horizontalalignment('center')
    ax_uv.tick_params(axis='x',labelsize=15)

    #出图——————————————————————————————————————————————————————————
    
    if(output_dir != None ):
        isExists=os.path.exists(output_dir)
        if not isExists:
            os.makedirs(output_dir)

        #output_dir2=output_dir+model+'_起报时间_'+initTime.strftime("%Y年%m月%d日%H时")+'/'
        #if(os.path.exists(output_dir2) == False):
        #    os.makedirs(output_dir2)

        plt.savefig(output_dir+extra_info['output_head_name']+
        initTime.strftime("%Y%m%d%H")+
        '00'+extra_info['output_tail_name']+'.jpg', dpi=200,bbox_inches='tight')
    else:
        plt.show()        