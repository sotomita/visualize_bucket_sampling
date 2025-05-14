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


def get_grad_sst(lon2d, lat2d, sst2d):
    dx, dy = mpcalc.lat_lon_grid_deltas(lon2d, lat2d)
    grad_y, grad_x = mpcalc.gradient(sst2d, deltas=(dy, dx))

    grad = np.sqrt(grad_x**2 + grad_y**2)

    return grad


if __name__ == "__main__":
    import namelist

    print("plot_sst_interp_grad.py")

    # read namelist
    plot_area = namelist.plot_area
    sst_min = namelist.grad_min
    sst_max = namelist.sst_max
    sst_delta = namelist.sst_delta
    grad_min = namelist.grad_min
    grad_max = namelist.grad_max
    grad_delta = namelist.grad_delta
    lon2d = namelist.lon2d
    lat2d = namelist.lat2d

    # read obs
    df = pd.read_csv("./sample/obs.csv", index_col=0)

    # interpolate SST
    sst2d = get_interp_sst(df["Lon"], df["Lat"], df["SST"], lon2d, lat2d)

    # calc norm of grad of SST
    sst_grad = get_grad_sst(
        lon2d * units("deg"), lat2d * units("deg"), sst2d * units("degC")
    )

    # plot
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
    gl.top_labels = False
    gl.right_labels = False

    ax1.add_feature(cfeature.COASTLINE, linewidth=0.8)

    cf = ax1.contourf(
        lon2d,
        lat2d,
        sst2d,
        cmap="turbo",
        vmin=sst_min,
        vmax=sst_max,
        transform=ccrs.PlateCarree(),
    )
    sc = ax1.scatter(
        df["Lon"],
        df["Lat"],
        c=df["SST"],
        cmap="turbo",
        vmin=sst_min,
        vmax=sst_max,
        edgecolors="black",
        linewidths=0.75,
        transform=ccrs.PlateCarree(),
    )
    cbar = fig.colorbar(
        sc,
        ax=ax1,
        orientation="vertical",
        location="left",
    )
    cbar.set_label("SST [degC]")
    cbar.ax.set_position([0.075, 0.2, 0.02, 0.5])

    c = ax1.contour(
        lon2d,
        lat2d,
        sst2d,
        colors="black",
        linewidths=0.75,
        transform=ccrs.PlateCarree(),
        levels=np.arange(sst_min, sst_max + sst_delta, sst_delta),
    )
    plt.clabel(c, fontsize=7)

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
    gl.top_labels = False
    gl.left_labels = False
    gl.right_labels = False

    ax2.add_feature(cfeature.COASTLINE, linewidth=0.8)

    cf = ax2.contourf(
        lon2d,
        lat2d,
        sst_grad * 1e4,
        cmap="binary",
        extend="max",
        levels=np.arange(grad_min, grad_max + grad_delta, grad_delta),
        transform=ccrs.PlateCarree(),
    )
    cbar = fig.colorbar(
        cf,
        ax=ax2,
        orientation="vertical",
        location="right",
    )
    cbar.set_label("|grad(SST)| [degC/10km]")
    cbar.ax.set_position([0.875, 0.2, 0.02, 0.5])

    c = ax2.contour(
        lon2d,
        lat2d,
        sst2d,
        colors="black",
        linewidths=0.75,
        transform=ccrs.PlateCarree(),
        levels=np.arange(sst_min, sst_max + sst_delta, sst_delta),
    )
    plt.clabel(c, fontsize=7)

    sc = ax2.scatter(
        df["Lon"],
        df["Lat"],
        c=df["SST"],
        cmap="turbo",
        vmin=sst_min,
        vmax=sst_max,
        edgecolors="black",
        linewidths=0.5,
        transform=ccrs.PlateCarree(),
    )

    # plt.tight_layout()
    plt.savefig("./fig.png")
