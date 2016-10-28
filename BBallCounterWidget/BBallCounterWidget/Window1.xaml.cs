using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using System.Windows.Threading;
using System.ComponentModel;
using System.IO;

using System.Net.Sockets;
using System.Net;

namespace BBallCounterWidget
{
    /// <summary>
    /// Interaction logic for Window1.xaml
    /// </summary>
    public partial class Window1 : Window
    {
        //Private variables
        Game game1;
        string serverIP;
        BackgroundWorker NetWorker;
        TcpClient client;
        NetworkStream stream;
        IPAddress address;
        const int port = 1005;
        StreamReader reader;
        StreamWriter writer;
        DispatcherTimer timer;


        private enum options
        {
            YES,
            YES_LATE,
            MAYBE,
            NO,
            UPDATE
        }

        public Window1()
        {
            InitializeComponent();
            this.Loaded += new RoutedEventHandler(Window1_Loaded);
            serverIP = "";

            NetWorker = new BackgroundWorker();
            NetWorker.DoWork += NetWorker_DoWork;
            client = null;
            reader = null;
            writer = null;
            address = IPAddress.Parse("127.0.0.1");
            stream = null;
            timer = new DispatcherTimer();
            timer.Interval = new TimeSpan(0, 15, 0);
            timer.IsEnabled = false;
            timer.Tick += timer_Tick;
        }

        void timer_Tick(object sender, EventArgs e)
        {
            NetWorker.RunWorkerAsync(options.UPDATE);
        }

        void Window1_Loaded(object sender, RoutedEventArgs e)
        {
            //Set the current value of the gauges
            game1 = new Game(0);
            this.myGauge1.DataContext = game1;

            
            //update gauge
            NetWorker.RunWorkerAsync(options.UPDATE);

           
        }

        private void Window_MouseDown(object sender, MouseButtonEventArgs e)
        {
            if (e.ChangedButton == MouseButton.Left)
                this.DragMove();
        }

        private void Window_Loaded(object sender, RoutedEventArgs e)
        {
            
        }

        private void Window_Initialized(object sender, EventArgs e)
        {
            this.IsEnabled = false;
        }

        private void close_Click(object sender, RoutedEventArgs e)
        {
            this.Close();
        }

        private void btnYes_Click(object sender, RoutedEventArgs e)
        {
            //update gauge
            NetWorker.RunWorkerAsync(options.YES);
        }

        private void btnYesLate_Click(object sender, RoutedEventArgs e)
        {
            //update gauge
            NetWorker.RunWorkerAsync(options.YES_LATE);
        }

        private void btnMaybe_Click(object sender, RoutedEventArgs e)
        {
            //update gauge
            NetWorker.RunWorkerAsync(options.MAYBE);
        }

        private void btnNo_Click(object sender, RoutedEventArgs e)
        {
            //update gauge
            NetWorker.RunWorkerAsync(options.UPDATE); //currently, ignoring no's on Form
        }

        private void btnUpdate_Click(object sender, RoutedEventArgs e)
        {
            //update gauge
            NetWorker.RunWorkerAsync(options.UPDATE);
        }

        void NetWorker_DoWork(object sender, DoWorkEventArgs eventArgs)
        {
            if (serverIP == "")
            {
                //get file
                try
                {
                    using (StreamReader reader = new StreamReader(@"\\nirvana.natinst.com\users\mshafer\bballCounterServer.ip"))
                    {
                        //get IP address
                        serverIP = reader.ReadLine().ToString();
                        //MessageBox.Show(serverIP);
                    }
                }
                catch
                {
                    MessageBox.Show(@"Could not access \\nirvana.natinst.com\users\msahfer\bballCounterServer.ip","Error: Could not get file");
                    //serverIP = "192.168.1.75";
                }
                
            }
            //establish connection to server - if not already there
            if (client == null)
            {
                client = new TcpClient(serverIP, port);
                stream = client.GetStream();
                reader = new StreamReader(stream);
                writer = new StreamWriter(stream) { AutoFlush = true };
            }

            //send query
            string message = "BBallCounter:";
            if (eventArgs.Argument.GetType() == typeof(options))
            {
                
                switch ((options)eventArgs.Argument)
                {
                    case (options.YES):
                        message += "YES";
                        break;
                    case (options.YES_LATE):
                        message += "Yes+-+Late";
                        break;
                    case (options.MAYBE):
                        message += "PROBABLY";
                        break;
                    case (options.UPDATE):
                        message += "UPDATE";
                        break;
                }

                writer.WriteLine(message);
            }

            //update gauge
            try
            {
                Byte[] Bytes =  System.Text.Encoding.ASCII.GetBytes(message);
               var data = new Byte[256];
                Int32 bytes = stream.Read(data, 0, data.Length);
                var responseData = System.Text.Encoding.ASCII.GetString(data, 0, bytes);
                string received = responseData;
                if (received.Substring(0, 12) == "BBallCounter")
                {

                    int count = Convert.ToInt32(received.Substring(13));
                    game1.Score = count;
                }
            }
            catch
            {
                //don't crash
            }

            client.Close();
            client = null;
            timer.IsEnabled = true;
            updateTime();
        }

        delegate void invoker();

        void updateTime()
        {
            if (!Dispatcher.CheckAccess())
            {
                Dispatcher.Invoke(new invoker(updateTime));
                return;
            }

            lblLastUpdate.Content = "Last updated: " + DateTime.Now.ToShortTimeString();
            this.IsEnabled = true;
        }
    }

    /// <summary>
    /// Helper class to simulate a game
    /// </summary>
    public class Game : INotifyPropertyChanged
    {
        private double score;

        public double Score
        {
            get { return score; }
            set
            {
                score = value;
                if (PropertyChanged != null)
                {
                    PropertyChanged(this, new PropertyChangedEventArgs("Score"));
                }
            }
        }


        public Game(double scr)
        {
            this.Score = scr;
        }


        #region INotifyPropertyChanged Members

        public event PropertyChangedEventHandler PropertyChanged;

        #endregion
    }
}
