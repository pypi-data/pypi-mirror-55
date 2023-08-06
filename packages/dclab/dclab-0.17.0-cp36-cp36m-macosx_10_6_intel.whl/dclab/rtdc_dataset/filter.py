#!/usr/bin/python
# -*- coding: utf-8 -*-
"""RT-DC dataset core classes and methods"""
from __future__ import division, print_function, unicode_literals

import warnings

import numpy as np

from dclab import definitions as dfn

from .. import downsampling
from ..polygon_filter import PolygonFilter


class Filter(object):
    def __init__(self, rtdc_ds):
        """Boolean filter arrays for RT-DC measurements

        Parameters
        ----------
        rtdc_ds: instance of RTDCBase
            The RT-DC dataset the filter applies to
        """
        # initialize important parameters
        self._init_rtdc_ds(rtdc_ds)
        # initialize properties
        self.reset()

    def __getitem__(self, key):
        """Return the filter for a feature in `self.features`"""
        if key in self.features and key in dfn.scalar_feature_names:
            if key not in self._filters:
                # Generate filters on-the-fly
                self._filters[key] = np.ones(self.size, dtype=bool)
        else:
            raise KeyError("Feature not available: '{}'".format(key))
        return self._filters[key]

    def _init_rtdc_ds(self, rtdc_ds):
        #: Available feature names
        self.features = rtdc_ds.features
        self.size = len(rtdc_ds)

    def reset(self):
        """Reset all filters"""
        # Box filters
        self._filters = {}
        #: All filters combined (see :func:`Filter.update`);
        #: Use this property to filter the features of
        #: :class:`dclab.rtdc_dataset.RTDCBase` instances
        self.all = np.ones(self.size, dtype=bool)
        #: Invalid (nan/inf) events
        self.invalid = np.ones(self.size, dtype=bool)
        #: 1D boolean array for manually excluding events; `False` values
        #: are excluded.
        self.manual = np.ones(self.size, dtype=bool)
        #: Polygon filters
        self.polygon = np.ones(self.size, dtype=bool)
        # old filter configuration of `rtdc_ds`
        self._old_config = {}

    def update(self, rtdc_ds, force=[]):
        """Update the filters according to `rtdc_ds.config["filtering"]`

        Parameters
        ----------
        rtdc_ds: dclab.rtdc_dataset.core.RTDCBase
            The measurement to which the filter is applied
        force : list
            A list of feature names that must be refiltered with
            min/max values.

        Notes
        -----
        This function is called when
        :func:`ds.apply_filter <dclab.rtdc_dataset.RTDCBase.apply_filter>`
        is called.
        """
        # re-initialize important parameters
        self._init_rtdc_ds(rtdc_ds)

        # These lists may help us become very fast in the future
        newkeys = []
        oldvals = []
        newvals = []

        cfg_cur = rtdc_ds.config["filtering"]
        cfg_old = self._old_config

        # Determine which data was updated
        for skey in list(cfg_cur.keys()):
            if skey not in cfg_old:
                cfg_old[skey] = None
            if cfg_cur[skey] != cfg_old[skey]:
                newkeys.append(skey)
                oldvals.append(cfg_old[skey])
                newvals.append(cfg_cur[skey])

        # 1. Filter all feature min/max values.
        # This line gets the feature names that must be filtered.
        col2filter = []
        for k in newkeys:
            # k[:-4] because we want to crop " min" and " max"
            if k[:-4] in dfn.scalar_feature_names:
                col2filter.append(k[:-4])

        for f in force:
            # Manually add forced features
            if f in dfn.scalar_feature_names:
                col2filter.append(f)
            else:
                # Make sure the feature name is valid.
                raise ValueError("Unknown feature name {}".format(f))

        col2filter = np.unique(col2filter)

        for col in col2filter:
            if col in rtdc_ds:
                fstart = col + " min"
                fend = col + " max"
                # Get the current feature filter
                col_filt = self[col]
                # If min and max exist and if they are not identical:
                if (fstart in cfg_cur and
                    fend in cfg_cur and
                        cfg_cur[fstart] != cfg_cur[fend]):
                    # TODO: speedup
                    # Here one could check for smaller values in the
                    # lists oldvals/newvals that we defined above.
                    # Be sure to check against force in that case!
                    ivalstart = cfg_cur[fstart]
                    ivalend = cfg_cur[fend]
                    if ivalstart > ivalend:
                        msg = "inverting filter: {} > {}".format(fstart, fend)
                        warnings.warn(msg)
                        ivalstart, ivalend = ivalend, ivalstart
                    data = rtdc_ds[col]
                    col_filt[:] = (ivalstart <= data)*(data <= ivalend)
                else:
                    col_filt[:] = True

        # 2. Filter with polygon filters
        # check if something has changed
        pf_id = "polygon filters"
        if (
            (pf_id in cfg_cur and pf_id not in cfg_old) or
            (pf_id in cfg_cur and pf_id in cfg_old and
             cfg_cur[pf_id] != cfg_old[pf_id])):
            self.polygon[:] = True
            # perform polygon filtering
            for p in PolygonFilter.instances:
                if p.unique_id in cfg_cur[pf_id]:
                    # update self.polygon
                    # iterate through axes
                    datax = rtdc_ds[p.axes[0]]
                    datay = rtdc_ds[p.axes[1]]
                    self.polygon *= p.filter(datax, datay)

        # 3. Invalid filters
        self.invalid[:] = True
        if cfg_cur["remove invalid events"]:
            for col in dfn.scalar_feature_names:
                if col in rtdc_ds:
                    data = rtdc_ds[col]
                    invalid = np.isinf(data) | np.isnan(data)
                    self.invalid *= ~invalid

        # 4. Finally combine all filters
        # get a list of all filters
        self.all[:] = True

        if cfg_cur["enable filters"]:
            for col in self._filters:
                self.all[:] *= self._filters[col]

            self.all[:] *= self.invalid
            self.all[:] *= self.manual
            self.all[:] *= self.polygon

            # Filter with configuration keyword argument "limit events".
            # This additional step limits the total number of events in
            # self.all.
            if cfg_cur["limit events"] > 0:
                limit = cfg_cur["limit events"]
                sub = self.all[self.all]
                _f, idx = downsampling.downsample_rand(sub,
                                                       samples=limit,
                                                       ret_idx=True)
                sub[~idx] = False
                self.all[self.all] = sub

        # Actual filtering is then done during plotting
        self._old_config = rtdc_ds.config.copy()["filtering"]
