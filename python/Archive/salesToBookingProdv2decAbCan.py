# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 08:49:45 2017

@author: Gary.Manley
"""
from win32com.client import Dispatch
import webbrowser
import pandas as pd
import datetime as datetime
import glob
import os
import zipfile 
import time
import urllib
from sqlalchemy import create_engine
import pyodbc as py
from shutil import copyfile
import win32com.client
import getpass
import xlwings as xw 
import sys
sys.path.append('S:\\10. MI\\Shared\\Python\\Other')
import XLFormatting as XL


#################
### Set the below to true or false to run required sections
#################

Fusion = False 
USS = True
Customer = False
Agents = False
SVP =  False

##############################
## Above imports
## Below Export and Reporting
##############################

runProc = True
export = True 
export2 = True
otherReporting = True
AbCanReports = True ### Will only run on a Tuesday even if True


#####turn on -see end to turn certain reports on and off
#######################################
experimental = True
### Handles Actual Sales Report 
### Called above as S2B being worked on
########################################





###############################
##### DO NOT SET TO TRUE
###############################
TCSExport = False ###  Set to yes to run only runs on specific day

input_dir = 'S:\\10. MI\\3. Gary Manley\\Reports\\Sales\\Sales To Bookings\\Input\\'


##################################################
#### gets current user used later for e-mail
#################################################
is_user = (getpass.getuser().replace('.',' ')).title()
is_userd = getpass.getuser()

### connec to Warehouse
conn_str = (
                   r'Driver={SQL Server};'
                   r'Server=TOTO-DWSQL01;'
                   r'Database=GMDB01;'
                   r'Trusted_Connection=yes;'
                       )   
quoted_conn_str = urllib.parse.quote_plus(conn_str)
engine = create_engine('mssql+pyodbc:///?odbc_connect={}'.format(quoted_conn_str))
cnxn = py.connect(conn_str)
cursor = cnxn.cursor() 

############################################
##### E-mail Function######################
###########################################

def email(reportname,attach,filename,mailistid): 
    xl = pd.ExcelFile('S:\\10. MI\\Shared\\Reports\\MailList\\ReportMailList.xlsx')
    dflist= xl.parse('Sheet1',index = 'ID')
    dfmail = dflist.loc[mailistid] #  TCS report
    dfmailcc = dflist.loc[0] #MI Team 
    dfmail = dfmail['MailList']
    dfmailcc = dfmailcc['MailList']

#####################
### e-mail
#####################
    const=win32com.client.constants
    olMailItem = 0x0
    obj = win32com.client.Dispatch("Outlook.Application")
    newMail = obj.CreateItem(olMailItem)

####################################
#### For Logo in Signiture
###################################
    attachment = newMail.Attachments.Add("S:\\10. MI\\Shared\\Reports\\Static\\Logo.png")
    imageCid = "Logo.png@123"
    attachment.PropertyAccessor.SetProperty("http://schemas.microsoft.com/mapi/proptag/0x3712001E", imageCid)

##################################
##Mail content
##################################
    newMail.Subject = reportname + "- " + str(datetime.datetime.today().strftime('%d/%m/%Y'))
    if attach:
        newMail.Attachments.Add(filename)
    newMail.HtmlBody = (r"""
                        <span style='font-size:12.0pt;font-family:Calabri;color:#212121'>                    
                        Hi All,<br> <br>
                        I have attached today's report. <br> <br>
                        Thanks, <br> <br>
                        </span>
                        <span style='font-size:12.0pt;font-family:"Arial",sans-serif;color:#212121'>"""+is_user+"""</span><span style='color:#212121'></span>
                        <br><b><span style='font-family:"Arial",sans-serif;color:#374696'>Data Analyst<o:p></o:p></span></p>
                        <span style='font-family:"Arial",sans-serif;color:#374696'>MI Department</span></b><span style='color:#212121'></span><br>
                        <b><span style='font-size:9.0pt;font-family:"Arial",sans-serif;color:#374696'>Email &amp; Skype:</span></b>
                        <span style='font-size:10.0pt;font-family:"Arial",sans-serif;color:#212121'><a href="mailto:"""+is_userd+"""@totoenergy.com">"""+is_userd+"""@totoenergy.com</a></span></p>
                        """+ "<body><img src=\"cid:{0}\"></body>".format(imageCid) + """
                        <span style='font-size:7.0pt;font-family:"Arial",sans-serif;color:#212121'>TOTO Energy is registered with Company Number 09256482</span><span style='color:#212121'></span></p>
                        <span style='font-size:7.0pt;font-family:"Arial",sans-serif;color:#212121'>Registered Office 1st Floor, Locksview, Brighton Marina, Brighton, BN2 5HA</span><span style='color:#212121'><o:p></o:p></span></p>
                        """)

##################################
### Set recipients to maillist
#################################
    newMail.To = dfmail
    newMail.CC = dfmailcc

################################
## Show E-mail 
################################

    newMail.display()

    


       
############################################
#### Function to process the fusion reports 
############################################
def fusion_save(name,first,last,con_MPAN,con_MPRN,date_cols):

######################
## Open Outlook
######################
    outlook = Dispatch("Outlook.Application").GetNamespace("MAPI")
    inbox = outlook.GetDefaultFolder("6")# "6" refers to the index of a folder. 6 is the inbox.
    all_inbox = inbox.Items.restrict("[ReceivedTime] > '"+datetime.datetime.today().strftime('%d/%m/%Y')+" 06:00 AM'") ### all inbox for today

###############
#find files
###############
    sub_today = 'FUSION Report'
# #   att_today = datetime.datetime.today().strftime('%Y%m%d') + ' COVE Gas Registration Tracking.csv'
    for msg in all_inbox:
       if sub_today in msg.Subject:
             if name in msg.body: 
                link = msg.body
                print(link)
                webbrowser.open(link) 
                break
    ### Find latest file matching report name wait 2 seconds to ensure download completed
    time.sleep(5)
    if 1==1:
    #try: 
        list_of_files = glob.glob('C:\\Users\\'+first+'.'+last+'\\Downloads\\*'+name+'*.zip') 
        latest_zip = max(list_of_files, key=os.path.getctime)         
        print(latest_zip)
        zip_ref = zipfile.ZipFile(latest_zip, 'r')
        zip_ref.extractall('C:\\Users\\'+first+'.'+last+'\\Downloads\\fusion')
        zip_ref.close()
        #### find csv unzipped
        list_of_csv_files = glob.glob('C:\\Users\\'+first+'.'+last+'\\Downloads\\fusion\\*'+name+'*.csv') 
        latest_csv = max(list_of_csv_files, key=os.path.getctime) 
        
        copyfile(latest_csv, 'S:\\10. MI\\Shared\\Reports\\Sales\\Sales to Bookings\\Daily Fusion Reports\\'+name+datetime.datetime.today().strftime('%d%m%Y')+'.csv')

        print(latest_csv)
        #### get data from the zipped file 
        if (con_MPAN and con_MPRN):
            repdata = pd.read_csv(latest_csv, encoding = "ISO-8859-1", dtype={'MPAN':float,'MPRN':float}, low_memory = False,skiprows=[0])
        if (con_MPAN and not con_MPRN):
            repdata = pd.read_csv(latest_csv, encoding = "ISO-8859-1", dtype={'MPAN':float}, low_memory = False,skiprows=[0])
        if (con_MPRN and not con_MPAN):
            repdata = pd.read_csv(latest_csv, encoding = "ISO-8859-1", dtype={'MPRN':float}, low_memory = False,skiprows=[0])
        if (not con_MPRN and not con_MPAN):
            repdata = pd.read_csv(latest_csv, encoding = "ISO-8859-1", low_memory = False,skiprows=[0])#, parse_dates = ['DATE'], dayfirst=False )
        if name == 'cancelled':
            repdata = pd.read_csv(latest_csv, encoding = "ISO-8859-1", dtype={'MPRN':float}, low_memory = False,skiprows=[0])
            repdata['CANCELLED_AT'] =  pd.to_datetime(repdata['CANCELLED_AT'], format='%d/%m/%Y %H:%M:%S')
            repdata['CANCELLED_AT'] = repdata['CANCELLED_AT'].dt.date
            repdata['DATE'] =  pd.to_datetime(repdata['DATE'], format='%d/%m/%Y %H:%M:%S')
            repdata['DATE'] = repdata['DATE'].dt.date
            repdata['BOOKED_ON'] =  pd.to_datetime(repdata['BOOKED_ON'], format='%d/%m/%Y %H:%M:%S')
            repdata['BOOKED_ON'] = repdata['BOOKED_ON'].dt.date
            #repdata['MPAN'] = repdata['MPAN'].astype(float)
            repdata['MPAN'] = repdata['MPAN'].apply(pd.to_numeric, errors='coerce')
            print(repdata.dtypes)
        
        for cols in date_cols.split(','):
            if name == 'cancelled' and cols == 'DATE':
                break
            #print(cols)
            repdata[cols] =  [pd.datetime.strptime(d, '%d/%m/%Y %H:%M:%S')  for d in repdata[cols]] 
            repdata[cols] =  repdata[cols].dt.date
        
        ##### is in all reports
        repdata['CUSTOMER_NUMBER'] = repdata['CUSTOMER_NUMBER'].apply(pd.to_numeric, errors='coerce')
        #### see what happens tomorrow !!!! 
        repdata['ACCOUNT_NUMBER'] = repdata['ACCOUNT_NUMBER'].apply(pd.to_numeric, errors='coerce')
        repdata['CONTACT_TELEPHONE_NUMBER'] = repdata['CONTACT_TELEPHONE_NUMBER'].apply(pd.to_numeric, errors='coerce')
        
       
        if name == 'overall-bookings': 
            repdata.to_sql(name='Booked', con=engine, if_exists = 'replace')
        if name == 'completed': 
            repdata.to_sql(name='stg_completed', con=engine, if_exists = 'replace')
            ##### cnxn.commit() add in ???? 
            cursor.execute("EXEC [dbo].[process_fusion] @Table = 'completed'")
        if name == 'abort': 
            repdata.to_sql(name='stg_aborted', con=engine, if_exists = 'replace')
            cursor.execute("EXEC [dbo].[process_fusion] @Table = 'aborted'")
        if name == 'cancelled': 
            repdata.to_sql(name='stg_cancelled', con=engine, if_exists = 'replace')
            cursor.execute("EXEC [dbo].[process_fusion] @Table = 'cancelled'")
        if name == 'in-progress': 
            repdata.to_sql(name='In_Progress', con=engine, if_exists = 'replace')

if Fusion: 
    first = 'gary'        
    last = 'manley'
    run = 'test'
    fusion_save('completed',first,last,True,True,"DATE,BOOKED_ON,COMPLETED_AT")
    fusion_save('abort',first,last,True,True,"DATE,BOOKED_ON,ABORTED_AT")
    fusion_save('in-progress',first,last,True,True,"DATE,BOOKED_ON")
    fusion_save('overall-bookings',first,last,True,True,"DATE,BOOKED_ON")
    fusion_save('cancelled',first,last,False,True,"DATE,BOOKED_ON,CANCELLED_AT")
#fusion_save('trip-out',first,last,True,True,"DATE,BOOKED_ON,COMPLETED_AT")



if USS:

##########################################################################################
#### Process the USS Reports ### These populate the tables under the views 
##########################################################################################

########################################
## Initiate Outlook inbox
## Fixed issue with picking up old files
#########################################
    outlook = Dispatch("Outlook.Application").GetNamespace("MAPI")
    inbox = outlook.GetDefaultFolder("6")# "6" refers to the index of a folder. 6 is the inbox.
    all_inbox = inbox.Items.restrict("[ReceivedTime] > '"+datetime.datetime.today().strftime('%d/%m/%Y')+" 07:00 AM'") ### all inbox for today
    val_date = datetime.datetime.today() ### Not sure used anymore 


##################
## Find elec file
##################
 
    sub_today = 'FW: TOTO Electric registration tracking report'
    att_today = datetime.datetime.today().strftime('%Y%m%d') + ' COVE Elec Registration Tracking.csv'
    for msg in all_inbox:
        if msg.Subject == sub_today:
            break

    for att in msg.Attachments:
        if att.FileName == att_today:
            break
    
    att.SaveAsFile(input_dir +'USS_Today_Elec.csv')    

###############
#find gas file
###############
    sub_today = 'FW: TOTO Gas registration tracking report'
    att_today = datetime.datetime.today().strftime('%Y%m%d') + ' COVE Gas Registration Tracking.csv'
    for msg in all_inbox:
        if msg.Subject == sub_today:
            break

    for att in msg.Attachments:
        if att.FileName == att_today:
            break
###############
#save gas file
###############
    att.SaveAsFile(input_dir + 'USS_Today_Gas.csv')
  
    frame = pd.read_csv(input_dir +'USS_Today_Elec.csv', encoding = "ISO-8859-1", dtype={'MPAN':float}, low_memory = False,skiprows=[0],parse_dates=[1,2], dayfirst=True)
    dfelec=pd.DataFrame(frame)
    dfelec.sort_values(by = ['MPAN','EFD'],ascending=[True,False], axis = 0, inplace = True)

    dfelec.to_sql(name='USSELEC', con=engine, if_exists = 'replace') 

##############################################################################
### change table name to USSELEC once working
#############################################################################


    frame = pd.read_csv(input_dir +'USS_Today_Gas.csv', encoding = "ISO-8859-1", low_memory = False,skiprows=[0],parse_dates=[2,3], dayfirst=True,dtype={'MPRN':float})
    dfgas=pd.DataFrame(frame)
    dfgas.sort_values(['MPRN','EFD','CONF_CYCLE'],ascending=[True,False,False], axis = 0, inplace = True)
    dfgas.to_sql(name='USSGAS', con=engine, if_exists = 'replace')


##########################################################################################
#### Process the Customer Details --- Elec Customer and Gas Customer
##########################################################################################

if Customer:
    print('Running Customer')
    dfCustElec = pd.read_table(input_dir+'Customer_Details_elec.txt', low_memory = False)
    print('Gas')
    dfCustGas = pd.read_table(input_dir+'Customer_Details_gas.txt', low_memory = False)
    print('Converting Data Types')
    dfCustElec['number1'] = dfCustElec['number1'].apply(pd.to_numeric, errors='coerce')
    dfCustGas['number1'] = dfCustGas['number1'].apply(pd.to_numeric, errors='coerce')
    dfCustElec['number2'] = dfCustElec['number2'].apply(pd.to_numeric, errors='coerce')
    dfCustGas['number2'] = dfCustGas['number2'].apply(pd.to_numeric, errors='coerce')
    dfCustElec['ElecPaymentReference'] = dfCustElec['ElecPaymentReference'].astype('str')
    dfCustGas['GasPaymentReference'] = dfCustGas['GasPaymentReference'].astype('str')
    print('importing data')
    dfCustElec.to_sql(name='Elec_Customer', con=engine, if_exists = 'replace')
    dfCustGas.to_sql(name='Gas_Customer', con=engine, if_exists = 'replace')


##########################################################################################
#### Process the Agents 
##########################################################################################

if Agents:
     print('Running Agents')
     list_of_files = glob.glob(input_dir+'Agent*.xlsx') 
     latest_file = max(list_of_files, key=os.path.getctime)
     dfAgent = pd.read_excel(latest_file, sheet_name = 'Agent'
                 )
     dfAgent.to_sql(name='Agent', con=engine, if_exists = 'replace')
##########################################################################################
#### Process the SVP Data
##########################################################################################

if SVP: 
     print('Running SVP')
     list_of_files = glob.glob(input_dir+'SVP_Data*.csv') 
     latest_file = max(list_of_files, key=os.path.getctime)
     dfSVP = pd.read_csv(latest_file, encoding = "ISO-8859-1", low_memory = False,parse_dates=[2,3,32], dayfirst=True#,dtype={'MPRN':float,'MPRN':float}
                 )
     dfSVP['MPAN'] = dfSVP['MPAN'].apply(pd.to_numeric, errors='coerce')
     dfSVP['MPRN'] = dfSVP['MPRN'].apply(pd.to_numeric, errors='coerce')
     dfSVP['datetimeStart'] =  pd.to_datetime(dfSVP['datetimeStart'], format='%d/%m/%Y %H:%M:%S')
     dfSVP['datetimeStart'] = dfSVP['datetimeStart'].dt.date
     
     dfSVP['verificationDate'] =  pd.to_datetime(dfSVP['verificationDate'], format='%d-%m-%Y %H:%M:%S')
     dfSVP['verificationDate'] = dfSVP['verificationDate'].dt.date
     
     dfSVP['Dates'] = dfSVP['datetimeStart']
     dfSVP.to_sql(name='SVP_Data_'+datetime.datetime.today().strftime('%d%m%Y'), con=engine, if_exists = 'replace')



Monday = False 
if datetime.datetime.today().weekday() == 0:
        Monday = True

Tuesday = False 
if datetime.datetime.today().weekday() == 1:
        Tuesday = True

Thursday = False 
if datetime.datetime.today().weekday() == 3:
        Thursday = True
        

if runProc:
    print('Running Proc')
    #Should normally be Y , only N if screwed up. 
    cursor.execute("EXEC [dbo].[Sales_To_Booking] @AddDupe = 'Y'")
    cnxn.commit()
    print('RunProc Complete')
   
    if Monday: 
        cursor.execute("EXEC [dbo].[S2B_MONDAY]")
        cnxn.commit()
    
    cursor.execute("EXEC [dbo].[DAILY_TRACKING]")
    cnxn.commit()
    
    
    
if export: 
  #  fd = open('S:\\10. MI\\3. Gary Manley\\Reports\\Sales\\Sales To Bookings\\Sql\\Summary_export.sql', 'r')
   # sqlFile = fd.read()##.decode('utf-16')
    #fd.close()
    ### this is for layak
    print('Running Export')
    dfExport = pd.read_sql('select * from v_summary_export_layak', cnxn ) #### change to _layak on end on 7/12/2017
    fname = 'S:\\10. MI\\Shared\\Reports\\Sales\\Sales To Bookings\\Summary Outputs\\Summary_'+datetime.datetime.today().strftime('%d%m%Y')+'.csv'
    dfExport.to_csv(fname,index = False)
    copyfile(fname, 'S:\\Smart Booking Reports\\Summary_'+datetime.datetime.today().strftime('%d%m%Y')+'.csv')
   # print (dfExport.head(5))
    
if export2: 
    print('Running Export')
    dfExport2 = pd.read_sql('select * from v_summary_export2', cnxn )
    fname = 'S:\\10. MI\\Shared\\Reports\\Sales\\Sales To Bookings\\Summary Outputs\\Summary2_'+datetime.datetime.today().strftime('%d%m%Y')+'.csv'
    dfExport2.to_csv(fname,index = False)
    

if otherReporting:
    cursor.execute("EXEC [dbo].[Bookings_Reconciliation]")
    #print('Bookings Recon Complete')
    cnxn.commit()
    dfExport = pd.read_sql('select * from v_bookings_recon order by 2 desc', cnxn )
    dfExport.to_csv('S:\\10. MI\\Shared\\Reports\\Sales\\Booking Source Report\\Outputs\\Bookings_Recon_Output_'+datetime.datetime.today().strftime('%d%m%Y')+'.csv',index = False)
    if Monday: 
        dfBookRec = dfExport
    cursor.execute("EXEC [dbo].[FUSION_CANCEL_LIST]")
    cnxn.commit()
    dfExport = pd.read_sql("SELECT * FROM Cancel_List", cnxn )
    dfExport.to_csv('S:\\2. Sales\\Onboarding Department\\Fusions Cancellations\\Fusion_Cancel_List'+datetime.datetime.today().strftime('%d%m%Y')+'.csv',index = False)
     
    if Monday: 
      dfExportCS = pd.read_sql("select * from Bookings_Recon where booking_Source in ('Toto CS','Field Sales') and Booked_On BETWEEN GETDATE()-7 AND GETDATE() order by 3 desc", cnxn )
      csfilename = 'S:\\Smart OPS\\Booking Source Reports\\Toto CS\\CS_Booking_Report_'+datetime.datetime.today().strftime('%d%m%Y')+'.csv'
      dfExportCS.to_csv(csfilename,index = False)
      
###### CANCEL AND ABORTED JUST ON A TUESDAY    
###### Bookings Recon on a Monday only 

if AbCanReports:
   if Tuesday: 
       
      #  cursor.execute("EXEC [dbo].[ABORT_LIST]")
        cursor.execute("EXEC [dbo].[P_ABORT_REPORT]")
        cursor.execute("EXEC [dbo].[COMPLETED_LIST]")
    #    cursor.execute("EXEC [dbo].[Cancelled_Reports_SP]")
        cursor.execute("EXEC [dbo].[P_CANCEL_REPORT]")
        
        cnxn.commit()
        
        dfExportAb = pd.read_sql("SELECT * FROM dbo.Abort_Report", cnxn )
    #    dfExportAb.to_csv('S:\\10. MI\\Shared\\Reports\\Sales\\Sales To Bookings\\Abort Report\\Output\\Abort_Report'+datetime.datetime.today().strftime('%d%m%Y')+'.csv',index = False)
        list_of_files = glob.glob('S:\\10. MI\\Shared\\Reports\\Sales\\Sales to Bookings\\Abort Report\\Abort_Report_*.xlsx') 
        latest_file = max(list_of_files, key=os.path.getctime)
        xw.App(visible=True)
        wb = xw.Book(latest_file)
        wb.sheets['Graph'].select()
        
        xw.Range('A1:B20').value = ''
        fd = open('S:\\10. MI\\Shared\\SQL\\Abort Report\\Overall_aborts.sql', 'r')
        sqlQuery = fd.read()
        fd.close()
        dfAbortCount = pd.read_sql_query(sqlQuery,engine )
        xw.Range('A1', index=False,header = True).value = dfAbortCount
        
        xw.Range('N1:V20').value = ''
        fd = open('S:\\10. MI\\Shared\\SQL\\Abort Report\\Abort_by_company.sql', 'r')
        sqlQuery = fd.read()
        fd.close()
        dfAbortCount = pd.read_sql_query(sqlQuery,engine )
        xw.Range('N1', index=False,header = True).value = dfAbortCount
        
        xw.Range('Y1:BN20').value = ''
        fd = open('S:\\10. MI\\Shared\\SQL\\Abort Report\\Abort_by_code.sql', 'r')
        sqlQuery = fd.read()
        fd.close()
        dfAbortCount = pd.read_sql_query(sqlQuery,engine )
        xw.Range('Y1', index=False,header = True).value = dfAbortCount
        
        xw.Range('BO1:MO100').value = ''
        fd = open('S:\\10. MI\\Shared\\SQL\\Abort Report\\Overall_aborts_patch.sql', 'r')
        sqlQuery = fd.read()
        fd.close()
        dfAbortCount = pd.read_sql_query(sqlQuery,engine )
        xw.Range('BO1', index=False,header = True).value = dfAbortCount #dfg
        
        wb.sheets['Patches by week'].select()
       
        ###### REFRESH PIVOT TABLES
        wb.api.ActiveSheet.PivotTables("PivotTable1").PivotCache().refresh()
        wb.api.ActiveSheet.PivotTables("PivotTable2").PivotCache().refresh()

        wb.sheets['PatchesSummary'].select()
        
        dfg = dfAbortCount[['Aborted', 'completed' ,'true_patch']].groupby(['true_patch'],as_index=False).agg(['sum'])
        dfg = dfg.reset_index()
    
        dfg = dfg.sort_values([('Aborted','sum')], ascending = False)
        dfg['Percent'] =  dfg['Aborted']/( dfg['Aborted']+ dfg['completed']) 
        
        xw.Range('A2', index=False,header = True).value = dfg
        wb.sheets('PatchesSummary').api.rows(3).EntireRow.Delete()
  
        wb.sheets['Abort_Report'].select()
        xw.Range('A1', index=False,header = True).value = dfExportAb
        xw.Range('M:M').WrapText = True
        xw.Range('M:M').WrapText = False
                
        wb.sheets['Abort_Type_Count'].select()
        fd = open('S:\\10. MI\\Shared\\SQL\\Abort Report\\AbortReportCount1.sql', 'r')
        sqlQuery = fd.read()
        fd.close()
        dfAbortCount = pd.read_sql_query(sqlQuery,engine )
        xw.Range('H1', index=False,header = True).value = dfAbortCount
        fd = open('S:\\10. MI\\Shared\\SQL\\Abort Report\\AbortReportCount2.sql', 'r')
        sqlQuery = fd.read()
        fd.close()
        dfAbortCount = pd.read_sql_query(sqlQuery,engine )
        
        wb.sheets['Customer_Abort_Patch_Count'].select()
        fd = open('S:\\10. MI\\Shared\\SQL\\Abort Report\\CustomerAbortPatchCount.sql', 'r')
        sqlQuery = fd.read()
        fd.close()
        dfAbortCount = pd.read_sql_query(sqlQuery,engine )
        xw.Range('A1', index=False,header = True).value = dfAbortCount   
        
        wb.sheets['Customer_Abort_Engineer_Count'].select()
        fd = open('S:\\10. MI\\Shared\\SQL\\Abort Report\\EngineerAbortPatchCount.sql', 'r')
        sqlQuery = fd.read()
        fd.close()
        dfAbortCount = pd.read_sql_query(sqlQuery,engine )
        xw.Range('A1', index=False,header = True).value = dfAbortCount       
        
        wb.sheets['Tech_Abort_Patch_Count'].select()
        fd = open('S:\\10. MI\\Shared\\SQL\\Abort Report\\TechAbortPatch.sql', 'r')
        sqlQuery = fd.read()
        fd.close()
        dfAbortCount = pd.read_sql_query(sqlQuery,engine )
        xw.Range('A1', index=False,header = True).value = dfAbortCount 
        
        wb.sheets['Tech_Abort_Engineer_Count'].select()
        fd = open('S:\\10. MI\\Shared\\SQL\\Abort Report\\TechAbortEng.sql', 'r')
        sqlQuery = fd.read()
        fd.close()
        dfAbortCount = pd.read_sql_query(sqlQuery,engine )
        xw.Range('A1', index=False,header = True).value = dfAbortCount 
        
        wb.sheets['Graph'].select()

       
        CFilename = 'S:\\10. MI\\Shared\\Reports\\Sales\\Sales to Bookings\\Abort Report\\Abort_Report_'+datetime.datetime.today().strftime('%d%m%Y')+'.xlsx'
        
        wb.save(CFilename)
        wb.close()
        
        
        cnxn.commit()
        dfExportCan = pd.read_sql("SELECT * FROM dbo.Cancel_Report", cnxn )
       # dfExportCan.to_csv('S:\\10. MI\\Shared\\Reports\\Sales\\Sales To Bookings\\Cancellation Report\\Output\\Cancel_Report'+datetime.datetime.today().strftime('%d%m%Y')+'.csv',index = False)
        
        list_of_files = glob.glob('S:\\10. MI\\Shared\\Reports\\Sales\\Sales to Bookings\\Cancellation Report\\Cancellation_Report_*.xlsx') 
        latest_file = max(list_of_files, key=os.path.getctime)
        xw.App(visible=True)
        wb = xw.Book(latest_file)
        wb.sheets['Raw Data'].select()
        xw.Range('A1', index=False,header = True).value = dfExportCan
                
        wb.sheets['Cancelled by Patch Count'].select()
        fd = open('S:\\10. MI\\Shared\\SQL\\Cancel Report\\CancelledReportCount1.sql', 'r')
        sqlQuery = fd.read()
        fd.close()
        dfAbortCount = pd.read_sql_query(sqlQuery,engine )
        xw.Range('A2', index=False,header = True).value = dfAbortCount

        wb.sheets['USS Status Count'].select()
        fd = open('S:\\10. MI\\Shared\\SQL\\Cancel Report\\GECount.sql', 'r')
        sqlQuery = fd.read()
        fd.close()
        dfAbortCount = pd.read_sql_query(sqlQuery,engine )
        xw.Range('A3', index=False,header = True).value = dfAbortCount
        
        fd = open('S:\\10. MI\\Shared\\SQL\\Cancel Report\\ECount.sql', 'r')
        sqlQuery = fd.read()
        fd.close()
        dfAbortCount = pd.read_sql_query(sqlQuery,engine )
        xw.Range('A12', index=False,header = True).value = dfAbortCount
        
        fd = open('S:\\10. MI\\Shared\\SQL\\Cancel Report\\GCount.sql', 'r')
        sqlQuery = fd.read()
        fd.close()
        dfAbortCount = pd.read_sql_query(sqlQuery,engine )
        xw.Range('A21', index=False,header = True).value = dfAbortCount
        
        
        wb.sheets['Graph Data'].select() 
        xw.Range('A1:B20').value = ''
        fd = open('S:\\10. MI\\Shared\\SQL\\Cancel Report\\Overall_cancel_patch.sql', 'r')
        sqlQuery = fd.read()
        fd.close()
        dfAbortCount = pd.read_sql_query(sqlQuery,engine )
        xw.Range('A1', index=False,header = True).value = dfAbortCount
        
        xw.Range('E1:I20').value = ''
        fd = open('S:\\10. MI\\Shared\\SQL\\Cancel Report\\Cancel_by_reason.sql', 'r')
        sqlQuery = fd.read()
        fd.close()
        dfAbortCount = pd.read_sql_query(sqlQuery,engine )
        xw.Range('E1', index=False,header = True).value = dfAbortCount
        
        xw.Range('L1:T20').value = ''
        fd = open('S:\\10. MI\\Shared\\SQL\\Cancel Report\\Cancel_by_company.sql', 'r')
        sqlQuery = fd.read()
        fd.close()
        dfAbortCount = pd.read_sql_query(sqlQuery,engine )
        xw.Range('L1', index=False,header = True).value = dfAbortCount

        xw.Range('W1:AB3000').value = ''      
        fd = open('S:\\10. MI\\Shared\\SQL\\Cancel Report\\PatchPivot.sql', 'r')
        sqlQuery = fd.read()
        fd.close()
        dfAbortCount = pd.read_sql_query(sqlQuery,engine )
        xw.Range('W1', index=False,header = True).value = dfAbortCount
        
        wb.sheets['ByPatch'].select()
        ws = wb.sheets['ByPatch']
        wb.api.ActiveSheet.PivotTables("PivotTable5").PivotCache().refresh()
        CaFilename = 'S:\\10. MI\\Shared\\Reports\\Sales\\Sales to Bookings\\Cancellation Report\\Cancellation_Report_'+datetime.datetime.today().strftime('%d%m%Y')+'.xlsx'
         
        wb.save(CaFilename)
        wb.close()

        email('Abort Report',True,CFilename,11)
        email('Cancel Report',True,CaFilename,12)
      
        
        
if TCSExport: 
   if Thursday: 
        dfExportTCS = pd.read_sql("select * from svp_data where SalesChannel = 'TPI / PCS' and Dates between dateadd(D,-14,GETDATE()) and GETDATE()", cnxn )
        filename = 'S:\\10. MI\\Shared\\Reports\\Sales\\TCS\\TCS_Report'+datetime.datetime.today().strftime('%d%m%Y')+'.csv'
        dfExportTCS.to_csv(filename,index = False)
        email('TCS',True,filename,6)
    
S2B = False 
Actual = True
CS = True 
BookingsRecon=True

## DATE AND FORMATTING

date = datetime.datetime.today().strftime('%d/%m/%Y')
date = [[datetime.datetime.strptime(date,'%d/%m/%Y')]]

###################################################
#Calculate todays date and import on the front tab
##################################################


if experimental:
    if S2B:
        dfExport2 = pd.read_sql('select * from v_summary_export2', cnxn )
        list_of_files = glob.glob('S:\\10. MI\\3. Gary Manley\\Reports\\Sales\\Sales To Bookings\\Sales to Booking Summary_*.xlsx') 
        latest_file = max(list_of_files, key=os.path.getctime)
        xw.App(visible=True)
        xw.App.calculation = 'manual'
        wb = xw.Book(latest_file)
        
        wb.api.Calculation= 'xlManual'
        wb.api.CalculateBeforeSave = False        
        
        wb.app.calculation = 'manual'
        wb.sheets['Forecast Target Summary'].select()
        wb.sheets['Forecast Target Summary'].range('C1').value = date
        wb.sheets['Summary'].select()
        xw.Range('A1', index=False,header = True).value = dfExport2
        wb.app.calculate()
        wb.sheets['Booked App Week 1-3 Status'].select()
        wb.api.ActiveSheet.PivotTables("PivotTable1").PivotCache().refresh()
        wb.sheets['Booked Under 5 Weeks'].select()
        wb.api.ActiveSheet.PivotTables("PivotTable2").PivotCache().refresh()
        wb.sheets['Forecast Target Summary'].select()
        #ws.PivotTables(j).PivotCache().Refresh()
        ### refresh pivots and replace formulas with values 
   
    if Actual: 
        list_of_files = glob.glob('S:\\10. MI\\Shared\\Reports\\Sales\\Actual Sales\\Actual Sales Report *.xlsx') 
        latest_file = max(list_of_files, key=os.path.getctime)
        xw.App(visible=True)
        dfExportA = pd.read_sql('select * from v_actual_sales', cnxn )
        wb = xw.Book(latest_file)
        wb.sheets['Summary'].select()
        xw.Range('A1', index=False,header = True).value = dfExportA
        wb.app.calculate()
        filename = 'S:\\10. MI\\Shared\\Reports\\Sales\\Actual Sales\\Actual Sales Report '+datetime.datetime.today().strftime('%d%m%y')+'.xlsx'
        wb.save(filename)
        wb.close()
        email('Actual Sales Report',True,filename,7)
    
    if CS: 
        if Monday:
            #### Comment Out when Completed 
          ##  dfExportCS = pd.read_sql("select * from Bookings_Recon where booking_Source in ('Toto CS','Field Sales') and Booked_On BETWEEN GETDATE()-7 AND GETDATE() order by 3 desc", cnxn )
            dfCSPivot = pd.read_sql("select booking_source as [Booking Source], BOOKED_BY as Advisor , COUNT(MPAN) Total from Bookings_Recon where booking_Source in ('Toto CS','Field Sales') and Booked_On BETWEEN GETDATE()-7 AND GETDATE() group by BOOKED_BY, booking_source",cnxn)
            rows = len(dfExportCS.index) 
            wb = xw.Book()
            xw.Range('A1', index=False,header = True).value = dfExportCS
            wb.api.ActiveSheet.Range("1:1").AutoFilter()
            xw.Range('A1:AI100').autofit()
            xw.sheets[0].api.Name = 'Detail' 
            XL.formatrange('A1:P'+str(rows+1),'Black','White',2,7,'A1:P'+str(rows+2),'Default')
            xw.Range('A:B').number_format = '0'
            
            wb.sheets.add('Pivot', before = 'Detail')
            wb.sheets['Pivot'].select()
            xw.Range('A1', index=False,header = True).value = dfCSPivot
            xw.Range('A1:AI100').autofit()
            wb.sheets['Pivot'].range('A1:AI1').api.Font.Bold = True
            filename = 'S:\\Smart OPS\\Booking Source Reports\\Toto CS__ '+datetime.datetime.today().strftime('%d%m%y')+'.xlsx'
            wb.save(filename)
            wb.close()
            email('Weekly CS Report',True,filename,8)
            
    if BookingsRecon: 
        if Monday:
            dfBookRec = pd.read_sql('select * from v_bookings_recon order by 2 desc', cnxn )
            list_of_files = glob.glob('S:\\10. MI\\Shared\\Reports\\Sales\\Booking Source Report\\Booking_Recon_Report_*.xlsx') 
            latest_file = max(list_of_files, key=os.path.getctime)
            xw.App(visible=True)
       
            wb = xw.Book(latest_file)
            wb.sheets['Total_Bookings'].select()
            xw.Range('A1', index=False,header = True).value = dfBookRec
            wb.app.calculate()
            wb.sheets['Booking Recon Dashboard'].select()
            filename = 'S:\\10. MI\\Shared\\Reports\\Sales\\Booking Source Report\\Booking_Recon_Report_ '+datetime.datetime.today().strftime('%d%m%y')+'.xlsx'
            wb.save(filename)
            wb.close()
            email('Bookings Recon Report',True,filename,10)  
            
            
            