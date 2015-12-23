#collectd#
---
###cookbook###
>[https://collectd.org/wiki/index.php/First_steps](https://collectd.org/wiki/index.php/First_steps "cook_book")
>[https://collectd.org/wiki/index.php/Plugin_architecture](https://collectd.org/wiki/index.php/Plugin_architecture "plugin_arch")
>[https://collectd.org/wiki/index.php/Value_list_t](https://collectd.org/wiki/index.php/Value_list_t)
>[https://collectd.org/wiki/index.php/Data_set_t](https://collectd.org/wiki/index.php/Data_set_t)
>[https://collectd.org/wiki/index.php/Inside_the_RRDtool_plugin](https://collectd.org/wiki/index.php/Inside_the_RRDtool_plugin)
>[https://github.com/collectd/collectd/blob/master/src/write_kafka.c](https://github.com/collectd/collectd/blob/master/src/write_kafka.c)
>[https://github.com/edenhill/librdkafka](https://github.com/edenhill/librdkafka)

###support kafka###
	git clone https://github.com/edenhill/librdkafka.git
 	cd librdkafka
	git checkout 0.8
	./configure
	make && make install
	cd <collectd_src_dir>
	./configure --enable-write_kafka
