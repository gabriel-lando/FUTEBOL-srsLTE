Changelog LandoNet
========

## lib/include/srslte/interfaces/enb_metrics_interface.h:
##### L50 - L57:
```
typedef struct {
  rf_metrics_t    rf;
  phy_metrics_t   phy[ENB_METRICS_MAX_USERS];
  mac_metrics_t   mac[ENB_METRICS_MAX_USERS];
  rrc_metrics_t   rrc; 
  s1ap_metrics_t  s1ap;
  bool            running;
}enb_metrics_t;
```
###### to:
```
typedef struct {
  rf_metrics_t    rf;
  phy_metrics_t   phy[ENB_METRICS_MAX_USERS];
  mac_metrics_t   mac[ENB_METRICS_MAX_USERS];
  rrc_metrics_t   rrc; 
  s1ap_metrics_t  s1ap;
  bool            running;
  float           tx_gain, rx_gain;
}enb_metrics_t;
```

## srsenb/src/metrics_stdout.cc:
##### L79 - L80:
```
    cout << "------DL------------------------------UL----------------------------------" << endl;
    cout << "rnti  cqi    ri   mcs  brate   bler   snr   phr   mcs  brate   bler    bsr" << endl;
```
###### to:
```
    cout << "------DL------------------------------UL-------------------------------------GAIN-----" << endl;
    cout << "rnti  cqi    ri   mcs  brate   bler   snr   phr   mcs  brate   bler    bsr   tx     rx" << endl;
```

## srsenb/src/enb.cc:
##### Add before ```m.running = started;``` (L291):
```
  m.tx_gain = radio.get_tx_gain();
  m.rx_gain = radio.get_rx_gain();
```

##### Add before ```cout << endl;``` (L133):
```
    // Print GAIN TX/RX
    cout << float_to_string(metrics.tx_gain, 2) << "";
    cout << float_to_string(metrics.rx_gain, 2) << "";
```

## srsepc/src/mme/nas.cc:
##### L1314:
```
  strncpy(emm_info.full_net_name.name, "Software Radio Systems LTE", LIBLTE_STRING_LEN);
```
###### to:
```
  strncpy(emm_info.full_net_name.name, "LandoNet LTE", LIBLTE_STRING_LEN);
```

##### L1317:
```
  strncpy(emm_info.short_net_name.name, "srsLTE", LIBLTE_STRING_LEN);
```
###### to:
```
  strncpy(emm_info.short_net_name.name, "LandoNet", LIBLTE_STRING_LEN);
```

## lib/include/srslte/radio/radio.h:
##### L153 - L159:
```
  const static double uhd_default_burst_preamble_sec = 600 * 1e-6;
  const static double uhd_default_tx_adv_samples = 98;
  const static double uhd_default_tx_adv_offset_sec = 4 * 1e-6;

  const static double blade_default_burst_preamble_sec = 0.0;
  const static double blade_default_tx_adv_samples = 27;
  const static double blade_default_tx_adv_offset_sec = 1e-6;
```
###### to:
```
  static constexpr double uhd_default_burst_preamble_sec = 600 * 1e-6;
  static constexpr double uhd_default_tx_adv_samples = 98;
  static constexpr double uhd_default_tx_adv_offset_sec = 4 * 1e-6;

  static constexpr double blade_default_burst_preamble_sec = 0.0;
  static constexpr double blade_default_tx_adv_samples = 27;
  static constexpr double blade_default_tx_adv_offset_sec = 1e-6;
```

## srsenb/hdr/phy/phch_worker.h:
##### L71 - L72:
```
  const static float PUSCH_RL_SNR_DB_TH = 1.0; 
  const static float PUCCH_RL_CORR_TH = 0.15;
```
###### to:
```
  static constexpr float PUSCH_RL_SNR_DB_TH = 1.0; 
  static constexpr float PUCCH_RL_CORR_TH = 0.15;
```

## srsue/hdr/phy/phch_recv.h:
##### L240:
```
  const static float ABSOLUTE_RSRP_THRESHOLD_DBM = -125;
```
###### to:
```
  static constexpr float ABSOLUTE_RSRP_THRESHOLD_DBM = -125;
```


## CMakeList.txt
##### L257:
```
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wno-comment -Wno-reorder -Wno-unused-but-set-variable -Wno-unused-variable -Wformat -Wmissing-field-initializers -Wtype-limits -std=c++03")
```
###### to:
```
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wno-comment -Wno-reorder -Wno-unused-but-set-variable -Wno-unused-variable -Wformat -Wmissing-field-initializers -Wtype-limits -std=c++17")
```


## srsenb/src/CMakeList.txt
##### L19:
```
target_link_libraries(srsenb  srsenb_upper
                              srsenb_mac
                              srsenb_phy
                              srslte_common
                              srslte_phy
                              srslte_upper
                              srslte_radio
                              rrc_asn1
                              ${CMAKE_THREAD_LIBS_INIT} 
                              ${Boost_LIBRARIES} 
                              ${SEC_LIBRARIES}
                              ${LIBCONFIGPP_LIBRARIES}
                              ${SCTP_LIBRARIES})
```
###### to:
```
target_link_libraries(srsenb  srsenb_upper
                              srsenb_mac
                              srsenb_phy
                              srslte_common
                              srslte_phy
                              srslte_upper
                              srslte_radio
                              rrc_asn1
                              ${CMAKE_THREAD_LIBS_INIT} 
                              ${Boost_LIBRARIES} 
                              ${SEC_LIBRARIES}
                              ${LIBCONFIGPP_LIBRARIES}
                              ${SCTP_LIBRARIES}
                              pistache)
```

## srsenb/src/main.cc:

##### Add before ```#include```:
```
// Add to Pistache Socket
#include <algorithm>

#include <pistache/http.h>
#include <pistache/router.h>
#include <pistache/endpoint.h>
#include <pistache/client.h>

using namespace Pistache;
using namespace Rest;

```

##### L347:
```
static bool do_metrics = false;
```
###### to:
```
static bool do_metrics = true;
```

##### L359 - L381:
```
void *input_loop(void *m)
{
  metrics_stdout *metrics = (metrics_stdout*) m;
  char key;
  while(running) {
    cin >> key;
    if (cin.eof() || cin.bad()) {
      cout << "Closing stdin thread." << endl;
      break;
    } else {
      if('t' == key) {
        do_metrics = !do_metrics;
        if(do_metrics) {
          cout << "Enter t to stop trace." << endl;
        } else {
          cout << "Enter t to restart trace." << endl;
        }
        metrics->toggle_print(do_metrics);
      }
    }
  }
  return NULL;
}
```
###### to:
```
void *input_loop(void *m)
{
  metrics_stdout *metrics = (metrics_stdout*) m;
  metrics->toggle_print(do_metrics);
  char key;
  while(running) {
    cin >> key;
    if (cin.eof() || cin.bad()) {
      cout << "Closing stdin thread." << endl;
      break;
    } else {
      if('t' == key) {
        do_metrics = !do_metrics;
        if(do_metrics) {
          cout << "Enter t to stop trace." << endl;
        } else {
          cout << "Enter t to restart trace." << endl;
        }
        metrics->toggle_print(do_metrics);
      }
    }
  }
  return NULL;
}
```

##### Add before ```main()```:
```
enb *enbLando;

namespace Lando {

  class ServerEndpoint {
  public:
      ServerEndpoint(Address addr)
          : httpEndpoint(std::make_shared<Http::Endpoint>(addr))
      { }

      void init(size_t thr = 2) {
          auto opts = Http::Endpoint::options()
              .threads(thr)
              .flags(Tcp::Options::InstallSignalHandler | Tcp::Options::ReuseAddr);
          httpEndpoint->init(opts);
          setupRoutes();
      }

      void start() {
          httpEndpoint->setHandler(router.handler());
          httpEndpoint->serveThreaded();
      }

      void shutdown() {
          httpEndpoint->shutdown();
      }

 private:
      void setupRoutes() {
          //using namespace Rest;

          Routes::Get(router, "/gain/:txgain/:rxgain", Routes::bind(&ServerEndpoint::doReceiveGain, this));

      }

      void doReceiveGain(const Rest::Request& request, Http::ResponseWriter response) {
          float txgain = request.param(":txgain").as<float>();
          float rxgain = request.param(":rxgain").as<float>();

          enbLando->radio.set_tx_gain(txgain);
          enbLando->radio.set_rx_gain(rxgain);

          cout << endl << "TX Gain set to = " << enbLando->radio.get_tx_gain() << endl;
          cout << "RX Gain set to = " << enbLando->radio.get_rx_gain() << endl << endl;

          response.send(Pistache::Http::Code::Ok, "Gain changed!\n");
      }

      std::shared_ptr<Http::Endpoint> httpEndpoint;
      Rest::Router router;
  };
}
```

##### Changes on ```main()``` function:
```
int main(int argc, char *argv[])
{
  signal(SIGINT, sig_int_handler);
  signal(SIGTERM, sig_int_handler);
  all_args_t        args;
  srslte::metrics_hub<enb_metrics_t> metricshub;
  metrics_stdout    metrics_screen;

  enb              *enb = enb::get_instance();

  srslte_debug_handle_crash(argc, argv);

  cout << "---  Software Radio Systems LTE eNodeB  ---" << endl << endl;

  parse_args(&args, argc, argv);
  if(!enb->init(&args)) {
    exit(1);
  }

  metricshub.init(enb, args.expert.metrics_period_secs);
  metricshub.add_listener(&metrics_screen);
  metrics_screen.set_handle(enb);

  srsenb::metrics_csv metrics_file(args.expert.metrics_csv_filename);
  if (args.expert.metrics_csv_enable) {
    metricshub.add_listener(&metrics_file);
    metrics_file.set_handle(enb);
  }

  // create input thread
  pthread_t input;
  pthread_create(&input, NULL, &input_loop, &metrics_screen);

  bool plot_started         = false; 
  bool signals_pregenerated = false; 
  if(running) {
    if (!plot_started && args.gui.enable) {
      enb->start_plot();
      plot_started = true; 
    }
  }
  int cnt=0;
  while (running) {
    if (args.expert.print_buffer_state) {
      cnt++;
      if (cnt==1000) {
        cnt=0;
        enb->print_pool();
      }
    }
    usleep(10000);
  }
  pthread_cancel(input);
  metricshub.stop();
  enb->stop();
  enb->cleanup();
  cout << "---  exiting  ---" << endl;
  exit(0);
}
```
###### to
```
int main(int argc, char *argv[])
{
  signal(SIGINT, sig_int_handler);
  signal(SIGTERM, sig_int_handler);
  all_args_t        args;
  srslte::metrics_hub<enb_metrics_t> metricshub;
  metrics_stdout    metrics_screen;

  enbLando = enb::get_instance();

  srslte_debug_handle_crash(argc, argv);

  cout << "---  Software Radio Systems LTE eNodeB  ---" << endl << endl;

  parse_args(&args, argc, argv);
  if(!enbLando->init(&args)) {
    exit(1);
  }

  metricshub.init(enbLando, args.expert.metrics_period_secs);
  metricshub.add_listener(&metrics_screen);
  metrics_screen.set_handle(enbLando);

  srsenb::metrics_csv metrics_file(args.expert.metrics_csv_filename);
  if (args.expert.metrics_csv_enable) {
    metricshub.add_listener(&metrics_file);
    metrics_file.set_handle(enbLando);
  }

  // create input thread
  pthread_t input;
  pthread_create(&input, NULL, &input_loop, &metrics_screen);

  bool plot_started         = false; 
  bool signals_pregenerated = false; 
  if(running) {
    if (!plot_started && args.gui.enable) {
      enbLando->start_plot();
      plot_started = true; 
    }
  }


  //Start REST API Pistache
  const int port = 9080;
  Pistache::Address addr(Pistache::Ipv4::any(), Pistache::Port(port));
  cout << endl << "Rest API runing at 0.0.0.0:" << port << endl << endl;
  Lando::ServerEndpoint serverLando(addr);

  serverLando.init();
  serverLando.start();

  signal(SIGABRT, sig_int_handler);
  signal(SIGTERM, sig_int_handler);
  signal(SIGINT, sig_int_handler);
  //REST API until here

  int cnt=0;
  while (running) {
    if (args.expert.print_buffer_state) {
      cnt++;
      if (cnt==1000) {
        cnt=0;
        enbLando->print_pool();
      }
    }
    usleep(10000);
  }

  serverLando.shutdown(); //Stop Pistache
  pthread_cancel(input);
  metricshub.stop();
  enbLando->stop();
  enbLando->cleanup();
  cout << "---  exiting  ---" << endl;
  exit(0);
}
```