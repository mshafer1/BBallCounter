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

using System.Threading;
using System.Threading.Tasks;

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
        const int port = 1005;
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
            timer = new DispatcherTimer();
            timer.Interval = new TimeSpan(0, 15, 0);
            timer.IsEnabled = false;
            timer.Tick += timer_Tick;            
            Thread.CurrentThread.Name = "Main";
        }

        void timer_Tick(object sender, EventArgs e)
        {
            Task A = new Task(() => update_server(options.UPDATE));
            A.Start();
            updateTime();
        }

        void Window1_Loaded(object sender, RoutedEventArgs e)
        {
            //Set the current value of the gauges
            game1 = new Game(0);
            this.myGauge1.DataContext = game1;


            //update gauge
            //NetWorker.RunWorkerAsync(options.UPDATE);
            Task A = new Task(() => setup_server());
            A.Start();
            A.Wait();
            if (serverIP == "")
            {
                throw new Exception("Error: Cannot find server");
            }

            A = new Task(() => update_server(options.UPDATE));
            A.Start();
            A.Wait();
            this.IsEnabled = true;
            timer.IsEnabled = true;
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
            Task A = new Task(() => update_server(options.YES));
            A.Start();
            updateTime();
        }

        private void btnYesLate_Click(object sender, RoutedEventArgs e)
        {
            //update gauge
            Task A = new Task(() => update_server(options.YES_LATE));
            A.Start();
            updateTime();
        }

        private void btnMaybe_Click(object sender, RoutedEventArgs e)
        {
            //update gauge
            Task A = new Task(() => update_server(options.MAYBE));
            A.Start();
            updateTime();
        }

        private void btnNo_Click(object sender, RoutedEventArgs e)
        {
            //update gauge
            Task A = new Task(() => update_server(options.NO));//currently, ignoring no's on Form
            A.Start();
            updateTime(); 
        }

        private void btnUpdate_Click(object sender, RoutedEventArgs e)
        {
            //update gauge
            Task A = new Task(() => update_server(options.UPDATE));
            A.Start();
            updateTime();
        }

        void setup_server()
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
                    MessageBox.Show(@"Could not access \\nirvana.natinst.com\users\msahfer\bballCounterServer.ip", "Error: Could not get file");
                    throw; //serverIP = "192.168.1.75";
                }
            }
        }

        void update_server(options input_var)
        {
            //while (Thread.CurrentThread.ThreadState == ThreadState.Running) ;
            TcpClient client;
            NetworkStream stream;
            IPAddress address;

            StreamReader reader;
            StreamWriter writer;
 

            //establish connection to server - if not already there
            try
            {
                client = new TcpClient(serverIP, port);
            }
            catch
            {
                MessageBox.Show("Could not connect to server - likely due to others trying to connect at the same time", "Error: Could not connect to server");
                return; //could not connect - likely due to an existing connection
            }
            stream = client.GetStream();
            reader = new StreamReader(stream);
            writer = new StreamWriter(stream) { AutoFlush = true };
            address = IPAddress.Parse("127.0.0.1");

            //send query
            string message = "BBallCounter:";
            if (input_var.GetType() == typeof(options))
            {

                switch ((options)input_var)
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
                    case (options.NO):
                        message += "NO";
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
                Byte[] Bytes = System.Text.Encoding.ASCII.GetBytes(message);
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
            
        }

        void NetWorker_DoWork(object sender, DoWorkEventArgs eventArgs)
        {
            
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

