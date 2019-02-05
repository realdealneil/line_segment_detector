#!/bin/bash
echo "Building test_fast_detector.cpp"
g++ `pkg-config --cflags opencv` test_fast_detector.cpp `pkg-config --libs opencv` -o test_fast_detector
