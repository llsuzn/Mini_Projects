using MahApps.Metro.Controls;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using System.Diagnostics;
using SmartHomeMonitoringApp.Views;
using MahApps.Metro.Controls.Dialogs;
using SmartHomeMonitoringApp.Logics;
using ControlzEx.Theming;

namespace SmartHomeMonitoringApp
{
    /// <summary>
    /// MainWindow.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class MainWindow : MetroWindow
    {
        string DefaultTheme { get; set; } = "Light";
        string DefaultAccent { get; set; } = "Purple";
        public MainWindow()
        {
            InitializeComponent();

            ThemeManager.Current.ThemeSyncMode = ThemeSyncMode.SyncWithAppMode;
            ThemeManager.Current.SyncTheme();
        }
        private void MetroWindow_Loaded(object sender, RoutedEventArgs e)
        {
            // <Frame> ==> Page.xaml
            // <ContentControl> ==> UserControl.xaml
            // ActiveItem.Content = new Views.DataBaseControl();
        }

        // 끝내기 버튼 클릭이벤트 핸들러
        private void MnuExitProgram_Click(object sender, RoutedEventArgs e)
        {
            Process.GetCurrentProcess().Kill(); // 작업관리자에서 프로세스 종료!
            Environment.Exit(0);    // 둘 중 하나만 쓰면 됨
        }

        // MQTT 시작메뉴 클릭 이벤트 핸들러
        private void MnuStartSubscribe_Click(object sender, RoutedEventArgs e)
        {
            var mqttPopWin = new MqttPopupWindow();
            mqttPopWin.Owner = this;
            mqttPopWin.WindowStartupLocation = WindowStartupLocation.CenterOwner;
            var result = mqttPopWin.ShowDialog();

            if (result == true)
            {
                var userControl = new Views.DataBaseControl();
                ActiveItem.Content = userControl;
                StsSelScreen.Content = "Database Monitoring"; //typeof(Views.DataBaseControl);
            }
        }

        private async void MetroWindow_Closing(object sender, System.ComponentModel.CancelEventArgs e)
        {
            // e.cancel을 true 하고 시작
            e.Cancel = true;

            var mySettings = new MetroDialogSettings
                                {
                                    AffirmativeButtonText = "끝내기",
                                    NegativeButtonText = "취소",
                                    AnimateShow = true,
                                    AnimateHide = true
                                };

            var result = await this.ShowMessageAsync("프로그램 끝내기", "프로그램을 끝내시겠습니까?",
                                                     MessageDialogStyle.AffirmativeAndNegative, mySettings);

            if(result == MessageDialogResult.Negative)
            {
                e.Cancel = true;
            }
            else if(result == MessageDialogResult.Affirmative)
            {
                if (Commons.MQTT_CLIENT != null && Commons.MQTT_CLIENT.IsConnected)
                {
                    Commons.MQTT_CLIENT.Disconnect();
                }
                Process.GetCurrentProcess().Kill(); // 가장 확실
            }
        }

        private void BtnExitProgram_Click(object sender, RoutedEventArgs e)
        {
            // 확인메시지 윈도우 클로징 이벤트 핸들러 호출
            this.MetroWindow_Closing(sender, new System.ComponentModel.CancelEventArgs());
        }

        private void MnuDataBaseMon_Click(object sender, RoutedEventArgs e)
        {
            ActiveItem.Content = new Views.DataBaseControl();
            StsSelScreen.Content = "Database Monitoring"; //typeof(Views.DataBaseControl);
        }

        private void MnuRealTimeMon_Click(object sender, RoutedEventArgs e)
        {
            ActiveItem.Content = new Views.RealTimeControl();
            StsSelScreen.Content = "RealTime Monitoring";
        }

        private void MnuVisualizationMon_Click(object sender, RoutedEventArgs e)
        {
            ActiveItem.Content = new Views.VisualizationControl();
            StsSelScreen.Content = "Visualization View";
        }

        private void MnuAbout_Click(object sender, RoutedEventArgs e)
        {
            var about = new About();
            about.Owner = this;
            about.ShowDialog();
        }

        //모든 테마와 액센트를 전부 처리할 체크 이벤트 핸들러
        private void MnuThemeAccent_Clicked(object sender, RoutedEventArgs e)
        {
            // 클릭되는 테마가 라이트인지 다크인지 판단 / 라이트를 클릭하면 다트는 체크해제, 다크를 클릭하면 라이트를 체크해제
            Debug.WriteLine((sender as MenuItem).Header);
            // 액센트도 체크를 하는 값을 나머지 액센트 전부 체크 해제

            switch ((sender as MenuItem).Header)
            {
                case "Light":
                    MnuLightTheme.IsCheckable = true;
                    MnuDarkTheme.IsCheckable = false;
                    DefaultTheme = "Light";
                    break;
                case "Dark":
                    MnuLightTheme.IsCheckable = false;
                    MnuDarkTheme.IsCheckable = true;
                    DefaultTheme = "Dark";
                    break;
                case "Amber":
                    MnuAccentMagenta.IsCheckable = true;
                    MnuAccentBlue.IsCheckable = false;
                    MnuAccentBrown.IsCheckable = false; 
                    MnuAccentCobalt.IsCheckable = false;
                    DefaultAccent = "Magenta";
                    break;
                case "Blue":
                    MnuAccentMagenta.IsCheckable = false;
                    MnuAccentBlue.IsCheckable = true;
                    MnuAccentBrown.IsCheckable = false;
                    MnuAccentCobalt.IsCheckable = false;
                    DefaultAccent = "Blue";
                    break;
                case "Brown":
                    MnuAccentMagenta.IsCheckable = false;
                    MnuAccentBlue.IsCheckable = false;
                    MnuAccentBrown.IsCheckable = true;
                    MnuAccentCobalt.IsCheckable = false;
                    DefaultAccent = "Brown";
                    break;
                case "Cobalt":
                    MnuAccentMagenta.IsCheckable = false;
                    MnuAccentBlue.IsCheckable = false;
                    MnuAccentBrown.IsCheckable = false;
                    MnuAccentCobalt.IsCheckable = true;
                    DefaultAccent = "Cobalt";
                    break;
            }

            ThemeManager.Current.ChangeTheme(this, $"{DefaultTheme}.{DefaultAccent}");
        }
    }
}
