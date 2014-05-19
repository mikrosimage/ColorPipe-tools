---
layout: post
title: "New release - v0.9"
date: "2014-01-24"
author: Marie FETIVEAU
version: v0.9
categories: [release]
---

**LUTLab**
* Add ACES colorspaces
* curve_to_lut : a command line tool to process a 1D LUT from a gradation function

**Utils**
* Helper functions to plot chromaticity coordinates in CIE1931 or CIE1976 diagrams

![gamuts_1976](https://f.cloud.github.com/assets/703797/1996789/4bf0221e-8519-11e3-8d94-320679ce8846.png)


**Web app**
* CherryPy web app has been refactored to anticipate the integration of LUTLab tools (like lut_to_lut for example)