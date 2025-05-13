#! /usr/bin/env/python3
# -*- encoding utf-8 -*-

import numpy as np
from scipy.interpolate import LinearNDInterpolator
import pandas as pd
import metpy.calc as mpcalc
from metpy.units import units
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature


def get_interp_sst(sample_lon, sample_lat, sample_sst, lon2d, lat2d) -> np.ndarray:
    f = LinearNDInterpolator(list(zip(sample_lon, sample_lat)), sample_sst)
    sst2d = f(lon2d, lat2d)

    return sst2d


if __name__ == "__main__":
    print("util.py")

    plot_area = [142, 145, 37, 42]

    lon = np.arange(141, 146, 0.05)
    lat = np.arange(36, 43, 0.05)
    lon2d, lat2d = np.meshgrid(lon, lat)

    df = pd.read_csv("./sample/obs.csv", index_col=0)

    sst2d = get_interp_sst(df["Lon"], df["Lat"], df["SST"], lon2d, lat2d)

    fig = plt.figure()
    ax1 = fig.add_subplot(
        1,
        2,
        1,
        projection=ccrs.Mercator(
            central_longitude=(plot_area[1] - plot_area[0]) * 0.5,
            min_latitude=plot_area[2],
            max_latitude=plot_area[3],
        ),
    )
    ax1.set_extent(plot_area)

    # grid lines and ticks
    gl = ax1.gridlines(
        crs=ccrs.PlateCarree(), color="gray", linestyle="--", draw_labels=True
    )

    ax1.add_feature(cfeature.COASTLINE, linewidth=0.8)

    cf = ax1.contourf(
        lon2d,
        lat2d,
        sst2d,
        cmap="turbo",
        vmin=5,
        vmax=16,
        transform=ccrs.PlateCarree(),
    )
    sc = ax1.scatter(
        df["Lon"],
        df["Lat"],
        c=df["SST"],
        cmap="turbo",
        vmin=5,
        vmax=16,
        edgecolors="black",
        linewidths=0.5,
        transform=ccrs.PlateCarree(),
    )
    cbar = fig.colorbar(
        sc,
        ax=ax1,
        orientation="vertical",
        location="left",
    )
    cbar.set_label("SST [degC]")

    ax2 = fig.add_subplot(
        1,
        2,
        2,
        projection=ccrs.Mercator(
            central_longitude=(plot_area[1] - plot_area[0]) * 0.5,
            min_latitude=plot_area[2],
            max_latitude=plot_area[3],
        ),
    )
    ax2.set_extent(plot_area)
    # grid lines and ticks
    gl = ax2.gridlines(
        crs=ccrs.PlateCarree(), color="gray", linestyle="--", draw_labels=True
    )

    ax2.add_feature(cfeature.COASTLINE, linewidth=0.8)

    c = ax2.contour(
        lon2d,
        lat2d,
        sst2d,
        colors="black",
        transform=ccrs.PlateCarree(),
    )

    plt.tight_layout()
    plt.savefig("./sample/fig.png")
