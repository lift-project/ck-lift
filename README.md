# CK-Lift repository

[![logo](https://github.com/ctuning/ck-guide-images/blob/master/logo-powered-by-ck.png)](https://github.com/ctuning/ck)
[![logo](https://github.com/ctuning/ck-guide-images/blob/master/logo-validated-by-the-community-simple.png)](http://cTuning.org)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

This is a [Collective Knowledge](http://cKnowledge.org) repository 
for the [Lift compiler](http://www.lift-project.org). It is used
to unify and automate installation and usage of the Lift compiler
across diverse platforms.

# Acknowledgedments

This work was supported by the [https://www.hipeac.net/mobility/collaborations HiPEAC collaboration grant] 
between the [http://www.ed.ac.uk University of Edinburgh] and [http://dividiti.com dividiti].

# Installation (Linux or Windows)

## Pre-requisities

* Python 2.7+ or 3.4+ with pip

## Setup

```
$ sudo pip install ck
$ ck pull repo --url=https://github.com/lift-project/ck-lift
```

## Test

```
$ ck install package --tags=compiler,lift
$ ck run lift-benchmark
```

# Next steps

We plan to integrate Lift with CK crowd-tuning technology
to crowdsource and speed up optimization of various math. algorithms
across diverse platforms and environments: http://cKnowledge.org/repo


# Feedback

Get in touch with Lift developers via official project website:
* http://lift-project.org

Get in touch with the CK community via this mailing list:
* http://groups.google.com/group/collective-knowledge
