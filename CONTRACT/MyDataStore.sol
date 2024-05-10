// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

contract MyDataStore {

    struct Measurement {
       string[] data;
       string[]   timestamp;
    }

    struct Channel {
       string id;
       mapping(string => Measurement) measurement;
    }

    mapping(string => Channel) channel_list;

    function put_data(string calldata channel, string calldata measurement, string calldata timestamp, string calldata data) public {
        Channel storage ch = channel_list[channel];
        ch.id = channel;
        Measurement storage m =  ch.measurement[measurement];
        m.data.push(data);
        m.timestamp.push(timestamp);
    }

    function get_data_num(string calldata channel, string calldata measurement) public view returns(uint) {
        Measurement memory data = channel_list[channel].measurement[measurement];
        return data.data.length;
    }
    function get_data(string calldata channel, string calldata measurement, uint start, uint stop) public view returns(Measurement memory) {
        Measurement memory data = channel_list[channel].measurement[measurement];
        Measurement memory m;
        uint data_num = data.data.length;
        if (start > data_num) {
            return m;
        }
        stop++;
        if (stop > data_num) {
            stop = data_num;
        }
        uint num = stop - start;
        m.data = new string[](num);
        m.timestamp = new string[](num);
        for (uint i = 0; i < num; i++) {
            m.data[i] = data.data[start+i];
            m.timestamp[i] = data.timestamp[start+i];
        }
        return m;
    }

}

