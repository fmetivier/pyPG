import matplotlib.cm as cm
import matplotlib.colors as colors
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection


from datetime import datetime
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

import numpy as np

from sqlalchemy import create_engine
from eralchemy import render_er

from copy import copy, deepcopy


mpl.rcParams["font.family"] = "monospace"
mpl.rcParams["font.size"] = 12


class Milestone:

    """Class to store Milestones informations for PERT diagrams"""

    def __init__(
        self,
        mid,
        mname,
        t,
        min_t,
        max_t,
        wp,
        pid,
        ax,
        min_mid,
        wp_step,
        mfcolor="C0",
        mecolor="C5",
    ):
        """initialization. stores the variables of the class

        :param    mid: milestone id
        :param    mname: milestone name
        :param    t: expected completion time
        :param    min_t: optimized completion time
        :param    max_t: bad completion time
        :param    wp: work package number
        :param    ax: matplotlib ax instance
        :param    min_mid: minimum mid of the wp used to calculate y-position of milesone names
        :param    wp_step: calculated x-position of milestone names
        :param    mfcolor: face color of the milestone
        :param    mecolor: edgecolor of the milestone
        """
        self.mid = mid  # milestone id
        self.mname = mname  # milestone name
        self.t = t  # milestone expected dat of completion
        self.min_t = min_t  # milestone min date of completion
        self.max_t = max_t  # milestone max date of completion if all goes wrong
        self.wp = wp  # milestone WP
        self.pid = pid  # milestone pid
        self.ax = ax
        self.wp_step = wp_step
        self.min_mid = min_mid
        self.present_wp = 1
        self.n_depends = 0
        self.mfcolor = mfcolor
        self.mecolor = mecolor
        self.add()

    def add(self):
        """
        plots the milsetone box
        """

        print(self.t, self.wp, self.mname)

        upper_names = str(self.mid) + "\n"
        middle_names = "\n\n" + str(self.t)
        lower_names = "\n\n\n\n" + str(self.min_t) + " | " + str(self.max_t)

        self.w = 2
        self.h = 2
        x = self.t - self.w / 2
        y = self.wp * 3 - self.h / 2
        self.x = x + self.w / 2
        self.y = y + self.h / 2

        rectangle = Rectangle(
            (x, y), self.w, self.h, edgecolor=self.mecolor, facecolor=self.mfcolor
        )
        self.ax.add_patch(rectangle)

        self.ax.text(
            self.t,
            self.wp * 3,
            upper_names,
            ha="center",
            va="center",
            fontsize=14,
            color="white",
            fontweight="heavy",
        )
        self.ax.text(
            self.t,
            self.wp * 3,
            middle_names,
            ha="center",
            va="center",
            fontsize=8,
            color="white",
        )
        self.ax.text(
            self.t, self.wp * 3, lower_names, ha="center", va="center", fontsize=8
        )

        if len(self.mname) > 20:
            tmp = self.mname.split(" ")
            l = len(tmp)
            self.mname = tmp[0]
            for i in range(len(tmp) - 1):
                if i < (len(tmp) - 2):
                    self.mname += " " + tmp[i + 1]
                else:
                    self.mname += (
                        "\n" + " " * len("(" + str(self.mid) + ") ") + tmp[i + 1]
                    )

        self.ax.text(
            (self.wp - 1) * self.wp_step,
            -(self.mid - self.min_mid) - 2,
            "(" + str(self.mid) + ") " + self.mname,
            ha="left",
        )

    def depends_on(self, x, y, mode="simple", n_arrows=2):
        """
        plots dependencies bewteen milestone instance and the milesone on
        which it depends


        :param    x,y: position of the center of milestone on which instance depends
        :param mode: direct connecting lines or more complex ones
        :param n_arrows: number of arrows to be drawn on connecting lines

        """
        if mode == "simple":
            xpos = [x, self.x]
            ypos = [y, self.y]
        else:
            xpos = [x, x + self.w / 2 + 0.5, x + self.w / 2 + 0.5, self.x]
            ypos = [y, y, self.y - 0.1 * self.n_depends, self.y - 0.1 * self.n_depends]

        self.ax.plot(xpos, ypos, "-", color="C5", zorder=-1)
        a_arrow = (self.y - y) / (self.x - x)

        for i in range(n_arrows):
            frac = 0.6 / n_arrows

            x_arrow = x + (0.2 + i * frac) * (self.x - x)
            y_arrow = y + a_arrow * (x_arrow - x)
            plt.arrow(
                x_arrow,
                y_arrow,
                0.1 * (self.x - x),
                0.1 * (self.y - y),
                shape="full",
                lw=0,
                length_includes_head=True,
                head_width=0.2,
                color="C5",
                zorder=-1,
            )

        self.n_depends += 1


def PERT(
    pid=1,
    db="myPERT",
    mylogin="root",
    mypass="iznogod01",
    chart_size=(18, 10),
    oname="PERT.pdf",
):
    """Draws a PERT chart using a Mariadb/mysql database and matplotlib

    :param  pid : project id in the database
    :param  db: name of the mysql database
    :param mylogin: login for database access
    :param mypass: pass database access
    :param  chart_size: figsize of the plt figure
    :param oname: outpout filename and extension

    """
    ##################
    # base connection
    ##################

    engine = create_engine("mysql://%s:%s@localhost/%s" % (mylogin, mypass, db))
    conn = engine.connect()

    ##################
    # queries
    ##################

    sql = "select count(distinct wid) from milestones where pid=%i" % (pid)
    wpc = conn.execute(sql).fetchall()[0][0]
    print(wpc)

    sql = "select * from  milestones where pid=%i" % (pid)
    ms = conn.execute(sql).fetchall()
    print(ms)
    plen = 36
    pos_step = int(plen / wpc)

    sql = "select wid, min(mid) from milestones where pid = %i group by wid" % (pid)
    miwp = conn.execute(sql).fetchall()
    pos_dic = {}
    for lines in miwp:
        pos_dic[lines[0]] = lines[1]

    sql = (
        "select max(N) from ( select wid, count(*) as N from milestones where pid=%i group by wid)  as Q"
        % (pid)
    )
    min_y = conn.execute(sql).fetchall()[0][0]

    sql = "select count(distinct wid) from milestones where pid=%i" % (pid)
    n_wp = conn.execute(sql).fetchall()[0][0]

    ##################
    # figure
    ##################
    fig, ax = plt.subplots(figsize=chart_size)

    milestones = []

    # milestones instanciation must be after figure as we send ax objet
    for m in ms:
        milestones.append(
            Milestone(
                m[0], m[1], m[2], m[3], m[4], m[5], m[6], ax, pos_dic[m[5]], pos_step
            )
        )

    ########################
    # Dependencies
    ########################
    sql = "select * from correl where pid=%i" % (pid)
    correl = conn.execute(sql).fetchall()
    for c in correl:
        milestones[c[0] - 1].depends_on(milestones[c[1] - 1].x, milestones[c[1] - 1].y)

    sql = "select * from wps where pid = %i" % (pid)
    wplist = conn.execute(sql).fetchall()
    c = 0
    tn = []
    for w in wplist:
        ax.text(0, w[0] * 3, "WP " + str(w[0]), ha="right")

    ########################
    # Time line
    ########################

    ax.plot([0, plen], [0, 0], "-", color="k")
    for i in np.arange(0, 42, 6):
        ax.plot(i, 0, "o", ms=6, color="k")
        ax.text(i, -0.6, str(i), ha="center")
    ax.text(plen / 2, 0.5, "Month", ha="center", va="center")

    # start end
    ax.plot(0, 0, "o", color="C5", ms=12)
    ax.plot(plen, 0, "o", color="C5", ms=12)
    ax.text(-0.25, 0, "Start", color="C5", ha="right", va="center")
    ax.text(plen + 0.25, 0, "End", color="C5", ha="left", va="center")

    ########################
    # axes
    ########################

    ax.set_ylim(-min_y, 3 * n_wp + 1)
    ax.yaxis.set_visible(False)
    ax.xaxis.set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)

    plt.savefig(oname, bbox_inches="tight")
    plt.show()


def GANTT(pid=1, db="myPERT", mylogin="root", mypass="iznogod01", oname="GANTT.pdf"):
    """draws GANTT chart using a Mariadb/mysql database

    :param pid: project id
    :param db: name of Mariadb/mysql dbase
    :param mylogin: login for database access
    :param mypass: pass database access
    :param oname: output filename and format
    """

    ##################
    # base connection
    ##################
    engine = create_engine("mysql://%s:%s@localhost/%s" % (mylogin, mypass, db))
    conn = engine.connect()

    plen = 36

    sql = "select count(distinct wpid) from wps where pid = %i" % (pid)
    n_wp = conn.execute(sql).fetchall()[0][0]

    sql = "select count(tid) from tasks where pid = %i group by wid " % (pid)
    res = conn.execute(sql).fetchall()
    n_t = 0
    for r in res:
        n_t += r[0]

    print(n_t)

    ##########################
    # figure size and axes
    ##########################

    ax = []
    fig = plt.figure(figsize=(15, 4 * n_wp))
    x0 = 0.1
    y0 = 0.1
    wtot = 0.85
    htot = 0.85
    spacing = 0.05

    ax.append(fig.add_axes([x0, y0, wtot, htot]))

    ht = (htot - n_wp * spacing) / n_t  # y-size of individual task

    hwp = y0
    for i in range(n_wp):
        ax.append(fig.add_axes([x0, hwp + spacing, wtot, ht * res[i][0]]))
        hwp += ht * res[i][0] + spacing

    sql = "select *  from wps where pid = %i" % (pid)
    res_wp = conn.execute(sql).fetchall()

    ##########################
    # plot GANTT
    ##########################

    # tasks
    for wp in res_wp:
        sql = "select * from tasks where wid=%i and pid = %i" % (wp[0], pid)
        t_list = conn.execute(sql).fetchall()
        Task_collection = []
        tnames = []

        for t in t_list:
            # print(t)
            x = t[4]
            w = t[5] - t[4]
            y = t[0]
            h = 0.6

            Task_collection.append(Rectangle((x, y - 0.3), w, h))
            ax[wp[0]].text(x - 0.5, y, t[1], ha="right", va="center")

        task_patch = PatchCollection(
            Task_collection, facecolor="C1", edgecolor="k", zorder=3
        )

        ax[wp[0]].add_collection(task_patch)

        #
        # add wp title
        #
        ax[wp[0]].plot([0, plen + 1], [y + 0.8, y + 0.8], "-", lw=2, color="lightgray")
        ax[wp[0]].text(
            0,  # plen / 2,
            y + 1.3,
            "WP-" + str(wp[0]) + " " + wp[1],
            fontsize=16,
            ha="left",  # "center",
            va="center",
        )

        #
        # Milestones and deliverables
        #
        # for overlapping milestones and delivrables we offset x by 1 month
        # using a dictionnary of monthes

        for t in t_list:
            month_list = {}
            sql = (
                "select * from milestones where wid = %i and pid = %i and tid='%s'"
                % (
                    wp[0],
                    pid,
                    t[0],
                )
            )
            milestones = conn.execute(sql).fetchall()

            for milestone in milestones:
                print(str(milestone[0]))
                x = milestone[2]
                if x in month_list.keys():
                    month_list[x] += 1
                    x += month_list[x] - 1
                else:
                    month_list[x] = 1

                print(milestone)
                ax[wp[0]].plot(x, milestone[7], ">", ms=20, mfc="C3", mec="k", zorder=3)
                ax[wp[0]].text(
                    x - 0.3,
                    milestone[7],
                    str(milestone[0]),
                    ha="left",
                    va="center",
                    color="white",
                    fontsize=7,
                )

            #
            # Deliverables
            #
            sql = "select * from deliverables where wid=%i and pid=%i and tid='%s'" % (
                wp[0],
                pid,
                t[0],
            )
            deliverables = conn.execute(sql).fetchall()
            for deliverable in deliverables:
                x = deliverable[5]
                if x in month_list.keys():
                    month_list[x] += 1
                    x += month_list[x] - 1
                else:
                    month_list[x] = 1

                ax[wp[0]].plot(
                    x,
                    deliverable[4],
                    "o",
                    ms=20,
                    mfc="C0",
                    mec="k",
                    zorder=3,
                )
                ax[wp[0]].text(
                    x,
                    deliverable[4],
                    deliverable[0],
                    ha="center",
                    va="center",
                    color="white",
                    fontsize=7,
                )

        ax[wp[0]].set_xlim(-1, plen + 1)
        ax[wp[0]].set_ylim(-0.5, y + 1)
        ax[wp[0]].yaxis.set_visible(False)
        ax[wp[0]].xaxis.set_visible(False)
        ax[wp[0]].spines["left"].set_visible(False)
        ax[wp[0]].spines["top"].set_visible(False)
        ax[wp[0]].spines["right"].set_visible(False)
        ax[wp[0]].spines["bottom"].set_visible(False)

    ax[0].set_xlim(-1, plen + 1)
    ax[0].set_ylim(-0.05, 1)
    ax[0].yaxis.set_visible(False)
    ax[0].xaxis.set_visible(False)
    ax[0].spines["left"].set_visible(False)
    ax[0].spines["top"].set_visible(False)
    ax[0].spines["right"].set_visible(False)
    ax[0].spines["bottom"].set_visible(False)

    ########################
    # Time line
    ########################

    ax[0].plot([0, plen], [0, 0], "-", color="k", zorder=5)
    for i in np.arange(0, plen + 6, 6):
        ax[0].plot(i, 0, "o", ms=6, color="k", zorder=5)
        ax[0].text(i, -0.03, str(i), ha="center", zorder=5)
    ax[0].text(plen / 2, -0.06, "Project month", ha="center", va="center", zorder=5)

    # start end
    ax[0].plot(0, 0, "o", color="C5", ms=12, zorder=5)
    ax[0].plot(plen, 0, "o", color="C5", ms=12, zorder=5)
    ax[0].text(-0.25, 0, "Start", color="C5", ha="right", va="center", zorder=5)
    ax[0].text(plen + 0.25, 0, "End", color="C5", ha="left", va="center", zorder=5)

    ########################
    # Legend
    ########################

    ax[0].plot(
        [],
        [],
        marker="s",
        ms=12,
        mfc="C1",
        mec="k",
        linestyle="None",
        label="Task",
    )
    ax[0].plot(
        [],
        [],
        marker=">",
        ms=10,
        mfc="C3",
        mec="k",
        linestyle="None",
        label="Milestone",
    )
    ax[0].plot(
        [],
        [],
        marker="o",
        ms=10,
        mfc="C0",
        mec="k",
        linestyle="None",
        label="Deliverable",
    )

    ax[0].legend(
        bbox_to_anchor=(0.3, -0.07, 0.4, 0.1),
        loc="lower left",
        ncol=3,
        mode="expand",
        borderaxespad=0.0,
    )

    plt.savefig(oname, bbox_inches="tight")
    plt.show()


if __name__ == "__main__":

    PERT()
    GANTT()
