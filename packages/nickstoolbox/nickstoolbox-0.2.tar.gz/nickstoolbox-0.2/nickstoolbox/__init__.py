################################################################################
# LIBRARIES USED
################################################################################
import resource                 # Used for Memory
import pydub 
import datetime 
import time 
import matplotlib.pyplot as plt 
import numpy as np 

name = "nickstoolbox"

################################################################################
# FUNCTIONS
################################################################################
#-------------------------------------------------------------------------------
def HowsMyMemory():
    print("TIME:    "+str(datetime.datetime.now()))
    print('Memory usage: %s (kb)' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
#-------------------------------------------------------------------------------
def EndCode():
    import time
    print('Code Ended at '+time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
#-------------------------------------------------------------------------------
def Scatter(x,y,z,c='b',marker='o',depthshade=True,xlabel='',ylabel='',zlabel=''):
    import numpy    as np
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x,y,z,c=c,marker=marker,depthshade=depthshade)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_zlabel(zlabel)
#-------------------------------------------------------------------------------
def ViewAvailableFonts():
    import matplotlib.font_manager
    list = matplotlib.font_manager.get_fontconfig_fonts()
    names = [matplotlib.font_manager.FontProperties(fname=fname).get_name() for fname in list]
    print(names)
    # ['Liberation Sans', 'DejaVu Sans', 'mry_KacstQurn', 'Lato', 'Lato', 'Tlwg Mono', 'Tlwg Typewriter', 'Umpush', 'FreeMono', 'Umpush', 'STIXVariants', 'NanumGothic', 'STIXSizeFourSym', 'KacstTitleL', 'Norasi', 'DejaVu Sans', 'Loma', 'Liberation Sans Narrow', 'Liberation Sans Narrow', 'Asgalt', 'KacstBook', 'DejaVu Sans', 'Norasi', 'DejaVu Serif', 'STIX', 'Sawasdee', 'Ubuntu Condensed', 'FreeSerif', 'Liberation Sans', 'KacstOffice', 'Umpush', 'STIXGeneral', 'FreeSans', 'Sawasdee', 'Umpush', 'Tlwg Typo', 'TakaoPGothic', 'FreeSans', 'Padauk Book', 'Minion Pro', 'Symbola', 'Waree', 'KacstOne', 'Lato', 'Lato', 'Tlwg Typo', 'Laksaman', 'STIXSizeThreeSym', 'DejaVu Sans', 'KacstArt', 'Liberation Mono', 'KacstPen', 'DejaVu Serif', 'Liberation Serif', 'Liberation Mono', 'Khmer OS System', 'Ubuntu', 'KacstQurn', 'STIXIntegralsSm', 'Ubuntu', 'Ubuntu Mono', 'Kinnari', 'STIXSizeOneSym', 'Tlwg Mono', 'Ubuntu Mono', 'NanumMyeongjo', 'STIXGeneral', 'KacstDecorative', 'Loma', 'Garuda', 'FreeSerif', 'Padauk', 'STIXSizeFiveSym', 'Ubuntu', 'Tlwg Typewriter', 'DejaVu Serif', 'Ubuntu', 'FreeMono', 'DejaVu Sans', 'Liberation Sans', 'Ubuntu', 'Norasi', 'STIXIntegralsUpSm', 'Laksaman', 'Lato', 'Liberation Serif', 'Lato', 'Warnock Pro', 'DejaVu Sans', 'DejaVu Sans Mono', 'TakaoPGothic', 'Waree', 'Liberation Sans', 'DejaVu Sans', 'STIXGeneral', 'Tlwg Typist', 'Norasi', 'STIXNonUnicode', 'Kinnari', 'Sylfaen', 'Khmer OS', 'Liberation Sans Narrow', 'Sawasdee', 'FreeSerif', 'Purisa', 'STIX Math', 'Liberation Mono', 'DejaVu Sans Mono', 'STIXIntegralsUpD', 'FreeSerif', 'Loma', 'Tlwg Typist', 'Lato', 'Tibetan Machine Uni', 'OpenSymbol', 'Liberation Serif', 'STIXSizeTwoSym', 'Sawasdee', 'Umpush', 'Waree', 'DejaVu Sans Mono', 'Lato', 'Waree', 'STIXVariants', 'Ubuntu', 'STIXSizeFourSym', 'Tlwg Mono', 'Lato', 'Ubuntu Mono', 'NanumMyeongjo', 'STIXNonUnicode', 'DejaVu Serif', 'Loma', 'Lato', 'Lato', 'DejaVu Sans', 'KacstDigital', 'KacstTitle', 'Liberation Sans Narrow', 'Garuda', 'Garuda', 'DejaVu Serif', 'NanumBarunGothic', 'STIX', 'Lato', 'Purisa', 'Lato', 'DejaVu Serif', 'DejaVu Sans', 'LKLUG', 'Tlwg Typo', 'Lato', 'KacstNaskh', 'STIXSizeThreeSym', 'KacstLetter', 'Tlwg Typist', 'Tlwg Typewriter', 'Ubuntu Mono', 'Kinnari', 'Norasi', 'Lato', 'STIXIntegralsUp', 'KacstOne', 'DejaVu Serif', 'Tlwg Typewriter', 'Bebas Neue', 'STIXIntegralsD', 'Kinnari', 'Purisa', 'Norasi', 'KacstFarsi', 'Laksaman', 'STIXIntegralsSm', 'STIX', 'DejaVu Serif', 'STIXGeneral', 'NanumBarunGothic', 'Abyssinica SIL', 'Lohit Punjabi', 'STIX', 'Lato', 'Kinnari', 'Liberation Serif', 'Padauk Book', 'Umpush', 'DejaVu Sans Mono', 'FreeMono', 'Phetsarath OT', 'STIXNonUnicode', 'Liberation Mono', 'Tlwg Mono', 'STIXIntegralsD', 'Saab', 'Tlwg Typo', 'FreeSans', 'FreeMono', 'NanumGothic', 'Tlwg Typist', 'Lato', 'Laksaman', 'STIXIntegralsUp', 'STIXSizeTwoSym', 'FreeSans', 'Ubuntu', 'KacstScreen', 'STIXIntegralsUpD', 'Kinnari', 'STIXSizeOneSym', 'STIXNonUnicode', 'KacstPoster', 'Padauk', 'Garuda', 'Purisa', 'Ubuntu', 'Lato', 'STIXIntegralsUpSm']
#-------------------------------------------------------------------------------
def ScatterWithHist(x, y, scatterstyle='bo', bin_no = None, cx = 'red', cy = 'cyan',alphaVal=0.5):
    # Description:
    #   This plots your xy plots but also puts in the histogram distribution of
    #   the x values on the x-axis and the histogram distribution of the y values
    #   on the y-axis.
    #   This was originally suggested by Dr. Gari Clifford as a sanity check to
    #   make sure that your data was properly distributed.
    fig, ax1 = plt.subplots()

    ax1.plot(x,y,scatterstyle)
    ax2 = ax1.twinx()
    ax2.hist(x,bins=bin_no,color=cx,orientation='vertical',alpha=alphaVal)
    ax3 = ax1.twiny()
    ax3.hist(y,bins=bin_no,color=cy,orientation='horizontal',alpha=alphaVal)

    # Set the colors of the axis the same as histogram
    ax1.set_xlabel('x',color = 'b')
    ax1.set_ylabel('y',color = 'b')
    ax2.set_ylabel(r'No. of Occurrences',color=cx)
    ax2.tick_params('y',colors=cx)
    ax3.set_xlabel(r'No. of Occurrences',color=cy)
    ax3.tick_params('x',colors=cy)
#-------------------------------------------------------------------------------
def ActivateLatex():
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
#-------------------------------------------------------------------------------
class Plot:
    def __init__(self):
        x = 1
    def ActivateLatex(self):
        plt.rc('text', usetex=True)
        plt.rc('font', family='serif')
    def SetTicks(self,size=20):
        plt.yticks(size=size)
        plt.xticks(size=size)

        #cax = plt.gcf().axes[0]
        #cax.tick_params(labelsize=size)

        plt.tight_layout()
#-------------------------------------------------------------------------------
def SetTicks(size=20):
    plt.yticks(size=size)
    plt.xticks(size=size)
#-------------------------------------------------------------------------------
def FlattenList(input_list):
    flat_list = []
    for sublist_or_el in input_list:
        if isinstance(sublist_or_el, list):
            for sublist_or_el2 in NicksToolbox.FlattenList(sublist_or_el):
                flat_list.append(sublist_or_el2)
        else:
            flat_list.append(sublist_or_el)
    return flat_list
#-------------------------------------------------------------------------------
def flatten(input_list):
    flat_list = []
    for sublist_or_el in input_list:
        if isinstance(sublist_or_el, list):
            for sublist_or_el2 in flatten(sublist_or_el):
                flat_list.append(sublist_or_el2)
        else:
            flat_list.append(sublist_or_el)
    return flat_list
#-------------------------------------------------------------------------------
def DrawBoundary(x,y):
    xmin = np.min(x); ymin = np.min(y)
    xmax = np.max(x); ymax = np.max(y)

    top_x = [xmin,xmax]
    top_y = [ymax,ymax]
    left_x =[xmin,xmin]
    left_y =[ymin,ymax]
    right_x=[xmax,xmax]
    right_y=[ymin,ymax]
    bot_x = [xmin,xmax]
    bot_y = [ymin,ymin]

    plt.plot(top_x,top_y,'k-')
    plt.plot(left_x,left_y,'k-')
    plt.plot(right_x,right_y,'k-')
    plt.plot(bot_x,bot_y,'k-')
#-------------------------------------------------------------------------------
class SendEmail():
    def __init__(self,msg,to,password=None):

        from string import Template
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        import smtplib
        from getpass import getpass
        MY_ADDRESS = input('What is your email? ')
        to = MY_ADDRESS
        if password is None:
            password = getpass()

        #Port Numbers for Gmail
        portSSL = 465
        portTLS = 587

        self.s = smtplib.SMTP(host='smtp.gmail.com',port = 587)
        self.s.starttls()
        self.s.login(MY_ADDRESS,password)

        #Initialize the message handle

        self.msg_handle = MIMEMultipart()

        #Setting up parameters of the email handle
        self.msg_handle['From'] = MY_ADDRESS
        self.msg_handle['To'] = to
        self.msg_handle['Subject']="Task has been completed"

        #Adding the message body
        self.msg_handle.attach(MIMEText(msg,'plain'))
    def send_message(self):
        self.s.send_message(self.msg_handle)
        self.s.quit()

#-------------------------------------------------------------------------------
class MP3:
    def read(self,f, normalized=False):
        """MP3 to numpy array"""
        a = pydub.AudioSegment.from_mp3(f)
        y = np.array(a.get_array_of_samples())
        if a.channels == 2:
            y = y.reshape((-1, 2))
        if normalized:
            return a.frame_rate, np.float32(y) / 2**15
        else:
            return a.frame_rate, y

    def write(self, f, sr, x, normalized=False):
        """numpy array to MP3"""
        channels = 2 if (x.ndim == 2 and x.shape[1] == 2) else 1
        if normalized:  # normalized array - each item should be a float in [-1, 1)
            y = np.int16(x * 2 ** 15)
        else:
            y = np.int16(x)
        song = pydub.AudioSegment(y.tobytes(), frame_rate=sr, sample_width=2, channels=channels)
        song.export(f, format="mp3", bitrate="320k")
#-------------------------------------------------------------------------------

