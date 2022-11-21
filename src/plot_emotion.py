# coding=utf-8
from __future__ import print_function

import numpy as np
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET


def plot_controllability():
    figure1, axis = plt.subplots(2, 2)
    x_loss = [abs(0.5 - 0.0), abs(0.75 - 0.5), abs(1.0 - 0.75), abs(0.0 - 0.75)]
    x_aversive = [abs(0.66 - 0.0), abs(0.33 - 0.66), abs(0.0 - 0.33), abs(1.0 - 0.33)]
    k = np.arange(-10, 10, 0.6)

    C_loss = [
        -(1 / abs(k * x_loss[0])) + x_loss[0] ** 2,
        -(1 / abs(k * x_loss[1])) + x_loss[1] ** 2,
        -(1 / abs(k * x_loss[2])) + x_loss[2] ** 2,
        -(1 / abs(k * x_loss[3])) + x_loss[3] ** 2,
    ]

    C_Aversive = [
        -(1 / abs(k * x_aversive[0])) + x_aversive[0] ** 2,
        -(1 / abs(k * x_aversive[1])) + x_aversive[1] ** 2,
        -(1 / abs(k * x_aversive[2])) + x_aversive[2] ** 2,
        -(1 / abs(k * x_aversive[3])) + x_aversive[3] ** 2,
    ]

    M_loss = [
        abs(k * x_loss[0]),
        abs(k * x_loss[1]),
        abs(k * x_loss[2]),
        abs(k * x_loss[3])
    ]

    M_Aversive = [
        abs(k * x_aversive[0]),
        abs(k * x_aversive[1]),
        abs(k * x_aversive[2]),
        abs(k * x_aversive[3])
    ]

    print("C_Aversive: \n {}".format(str(C_Aversive)))
    print("C_Loss: \n {}".format(str(C_loss)))
    print("M_Aversive: \n {}".format(str(M_Aversive)))
    print("M_loss: \n {}".format(str(M_loss)))
    return

    # Controllability Loss
    axis[0, 0].set_title('Controllability C(K) Loss')
    axis[0, 0].plot(k, C_loss[0], linestyle='--', color='magenta', marker='o',
                    label=u'Start \u0394(L) = ' + str(x_loss[0]))
    axis[0, 0].plot(k, C_loss[1], linestyle='--', color='blue', marker='v',
                    label=u'Middle \u0394(L) = ' + str(x_loss[1]))
    axis[0, 0].plot(k, C_loss[2], linestyle='--', color='red', marker='+', label=u'Bad \u0394(L) = ' + str(x_loss[2]))
    axis[0, 0].plot(k, C_loss[3], linestyle='--', color='green', marker='x',
                    label=u'Good \u0394(L) = ' + str(x_loss[3]))
    axis[0, 0].grid()
    axis[0, 0].legend(loc='lower left')

    axis[0, 0].set_xlabel(r'$K\;\rightarrow$')
    axis[0, 0].set_ylabel(r'$C(K)\longrightarrow$')
    axis[0, 0].axhline(0, color='black')
    axis[0, 0].axvline(0, color='black')

    # Changeability Loss
    axis[0, 1].set_title('Changeability M(K) Loss')
    axis[0, 1].plot(k, M_loss[0], linestyle='--', color='magenta', marker='o',
                    label=u'Start \u0394(L) = ' + str(x_loss[0]))
    axis[0, 1].plot(k, M_loss[1], linestyle='--', color='blue', marker='v',
                    label=u'Middle \u0394(L) = ' + str(x_loss[1]))
    axis[0, 1].plot(k, M_loss[2], linestyle='--', color='red', marker='+', label=u'Bad \u0394(L) = ' + str(x_loss[2]))
    axis[0, 1].plot(k, M_loss[3], linestyle='--', color='green', marker='x',
                    label=u'Good \u0394(L) = ' + str(x_loss[3]))
    axis[0, 1].grid()
    axis[0, 1].legend(loc='lower left')

    axis[0, 1].set_xlabel(r'$K\;\rightarrow$')
    axis[0, 1].set_ylabel(r'$M(K)\longrightarrow$')
    axis[0, 1].axhline(0, color='black')
    axis[0, 1].axvline(0, color='black')

    # Controllability Aversive
    axis[1, 0].set_title('Controllability C(K) Aversive')
    axis[1, 0].plot(k, C_Aversive[0], linestyle='--', color='magenta', marker='o',
                    label=u'Start \u0394(L) = ' + str(x_aversive[0]))
    axis[1, 0].plot(k, C_Aversive[1], linestyle='--', color='blue', marker='v',
                    label=u'Middle \u0394(L) = ' + str(x_aversive[1]))
    axis[1, 0].plot(k, C_Aversive[2], linestyle='--', color='red', marker='+',
                    label=u'Bad \u0394(L) = ' + str(x_aversive[2]))
    axis[1, 0].plot(k, C_Aversive[3], linestyle='--', color='green', marker='x',
                    label=u'Good \u0394(L) = ' + str(x_aversive[3]))
    axis[1, 0].grid()
    axis[1, 0].legend(loc='lower left')

    axis[1, 0].set_xlabel(r'$K\;\rightarrow$')
    axis[1, 0].set_ylabel(r'$C(K)\longrightarrow$')
    axis[1, 0].axhline(0, color='black')
    axis[1, 0].axvline(0, color='black')

    # Changeability Aversive
    axis[1, 1].set_title('Changeability M(K) Aversive')
    axis[1, 1].plot(k, M_Aversive[0], linestyle='--', color='magenta', marker='o',
                    label=u'Start \u0394(L) = ' + str(x_aversive[0]))
    axis[1, 1].plot(k, M_Aversive[1], linestyle='--', color='blue', marker='v',
                    label=u'Middle \u0394(L) = ' + str(x_aversive[1]))
    axis[1, 1].plot(k, M_Aversive[2], linestyle='--', color='red', marker='+',
                    label=u'Bad \u0394(L) = ' + str(x_aversive[2]))
    axis[1, 1].plot(k, M_Aversive[3], linestyle='--', color='green', marker='x',
                    label=u'Good \u0394(L) = ' + str(x_aversive[3]))
    axis[1, 1].grid()
    axis[1, 1].legend(loc='lower left')

    axis[1, 1].set_xlabel(r'$K\;\rightarrow$')
    axis[1, 1].set_ylabel(r'$M(K)\longrightarrow$')
    axis[1, 1].axhline(0, color='black')
    axis[1, 1].axvline(0, color='black')

    # Combine all the operations and display
    plt.tight_layout()
    plt.show()


def plot_emotion():
    figure1, axis = plt.subplots(2, 2)
    xticks_bad = ['Start', 'Middle', 'Bad']
    xticks_good = ['Start', 'Middle', 'Good']
    x = np.array([0, 1, 2])

    """ Get all data from XML files
    label = "intensity_emotions_"
    files = [label + "Aversive-Start.xml", label + "Aversive-Middle.xml", label + "Aversive-Bad.xml", label + "Aversive-Good.xml",
             label + "Loss-Start.xml", label + 'Loss-Middle.xml', label + "Loss-Bad.xml", label + "Loss-Good.xml"]
    intensity = []

    for file in files:
        xml_log = ET.parse(file)
        root = xml_log.getroot()

        for emotion in root.findall('emotion'):
            value = emotion.find('intensity').text
            intensity.append()"""

    # First graph Loss condition with Bad outcome
    angry_loss_bad = np.array([4.512055046365087, 4.512055046365087, 4.344971374671305])
    sad_loss_bad = np.array([3.885667863197372, 3.885667863197372, 3.997191443993421])
    afraid_loss_bad = np.array([4.387485827828359, 4.387485827828359, 4.073818322357865])
    happy_loss_bad = np.array([3.3415567456865523, 3.3415567456865523, 2.9299381047901])
    annoyed_loss_bad = np.array([4.549055774574677, 4.549055774574677, 4.406151323989015])

    axis[0, 0].set_title('Loss with Bad outcome')
    axis[0, 0].set_xticks(x)
    axis[0, 0].set_xticklabels(xticks_bad)
    axis[0, 0].plot(x, angry_loss_bad, linestyle='--', color='red', marker='o', label="Angry")
    axis[0, 0].plot(x, sad_loss_bad, linestyle='--', color='blue', marker='v', label="Sad")
    axis[0, 0].plot(x, afraid_loss_bad, linestyle='--', color='magenta', marker='+', label="Afraid")
    axis[0, 0].plot(x, happy_loss_bad, linestyle='--', color='gold', marker='x', label="Happy")
    axis[0, 0].plot(x, annoyed_loss_bad, linestyle='--', color='green', marker='s', label="Annoyed")
    axis[0, 0].grid()

    # Second graph Loss condition with Good outcome
    angry_loss_good = np.array([4.512055046365087, 4.512055046365087, 3.781876298545688])
    sad_loss_good = np.array([3.885667863197372, 3.885667863197372, 3.088703899810312])
    afraid_loss_good = np.array([4.387485827828359, 4.387485827828359, 4.0917589852172265])
    happy_loss_good = np.array([3.3415567456865523, 3.3415567456865523, 4.426544340239439])
    annoyed_loss_good = np.array([4.549055774574677, 4.549055774574677, 3.749879587204018])

    axis[0, 1].set_title('Loss with Good outcome')
    axis[0, 1].set_xticks(x)
    axis[0, 1].set_xticklabels(xticks_good)
    axis[0, 1].plot(x, angry_loss_good, linestyle='--', color='red', marker='o', label="Angry")
    axis[0, 1].plot(x, sad_loss_good, linestyle='--', color='blue', marker='v', label="Sad")
    axis[0, 1].plot(x, afraid_loss_good, linestyle='--', color='magenta', marker='+', label="Afraid")
    axis[0, 1].plot(x, happy_loss_good, linestyle='--', color='gold', marker='x', label="Happy")
    axis[0, 1].plot(x, annoyed_loss_good, linestyle='--', color='green', marker='s', label="Annoyed")
    axis[0, 1].grid()

    # Third graph Aversive condition with Bad outcome
    angry_aversive_bad = np.array([4.476106853425577, 4.512029736874062, 4.344580772926913])
    sad_aversive_bad = np.array([3.7768426500384242, 3.885925675652677, 3.9972349964430864])
    afraid_aversive_bad = np.array([4.487489947142326, 4.387131720350737, 4.073321209701658])
    happy_aversive_bad = np.array([3.550554372350415, 3.340980997798731, 2.9293591728194914])
    annoyed_aversive_bad = np.array([4.489125130229521, 4.549093208339125, 4.405769696480293])

    axis[1, 0].set_title('Aversive with Bad outcome')
    axis[1, 0].set_xticks(x)
    axis[1, 0].set_xticklabels(xticks_bad)
    axis[1, 0].plot(x, angry_aversive_bad, linestyle='--', color='red', marker='o', label="Angry")
    axis[1, 0].plot(x, sad_aversive_bad, linestyle='--', color='blue', marker='v', label="Sad")
    axis[1, 0].plot(x, afraid_aversive_bad, linestyle='--', color='magenta', marker='+', label="Afraid")
    axis[1, 0].plot(x, happy_aversive_bad, linestyle='--', color='gold', marker='x', label="Happy")
    axis[1, 0].plot(x, annoyed_aversive_bad, linestyle='--', color='green', marker='s', label="Annoyed")
    axis[1, 0].grid()

    # Forth graph Aversive condition with Good outccome
    angry_aversive_good = np.array([4.476106853425577, 4.512029736874062, 3.855045836589355])
    sad_aversive_good = np.array([3.7768426500384242, 3.885925675652677, 3.1566866516063805])
    afraid_aversive_good = np.array([4.487489947142326, 4.387131720350737, 4.158435433614303])
    happy_aversive_good = np.array([3.550554372350415, 3.340980997798731, 4.355774553252712])
    annoyed_aversive_good = np.array([4.489125130229521, 4.549093208339125, 3.8244736363717733])

    axis[1, 1].set_title('Aversive with Good outcome')
    axis[1, 1].set_xticks(x)
    axis[1, 1].set_xticklabels(xticks_good)
    axis[1, 1].plot(x, angry_aversive_good, linestyle='--', color='red', marker='o', label="Angry")
    axis[1, 1].plot(x, sad_aversive_good, linestyle='--', color='blue', marker='v', label="Sad")
    axis[1, 1].plot(x, afraid_aversive_good, linestyle='--', color='magenta', marker='+', label="Afraid")
    axis[1, 1].plot(x, happy_aversive_good, linestyle='--', color='gold', marker='x', label="Happy")
    axis[1, 1].plot(x, annoyed_aversive_good, linestyle='--', color='green', marker='s', label="Annoyed")
    axis[1, 1].grid()

    # Combine all the operations and display
    plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
    plt.tight_layout()
    plt.show()


def plot_appraisal():
    figure1, axis = plt.subplots(4, 2)
    xticks = ['Start', 'Middle']
    x = np.array([0, 1])

    # First graph Aversive Controllability
    modal_c = np.array([1.60037373737, 0.0654974747475])
    ema_c = np.array([3.25, 1.6])
    scpq_c = np.array([3.15, 2.73])

    axis[0, 0].set_title('Aversive Controllability')
    axis[0, 0].set_xticks(x)
    axis[0, 0].set_xticklabels(xticks)
    axis[0, 0].set_ylim([0, 5])
    axis[0, 0].plot(x, modal_c, linestyle='--', color='green', marker='o', label="The Proposed Model")
    axis[0, 0].plot(x, ema_c, linestyle='--', color='purple', marker='x', label="EMA")
    axis[0, 0].plot(x, scpq_c, linestyle='--', color='red', marker='v', label="SCPQ")
    axis[0, 0].grid()

    # Second graph Aversive Changeability
    modal_ch = np.array([1.1, 0.55])
    ema_ch = np.array([3.4, 1.2])
    scpq_ch = np.array([1.76, 1.51])

    axis[1, 0].set_title('Aversive Changeability')
    axis[1, 0].set_xticks(x)
    axis[1, 0].set_xticklabels(xticks)
    axis[1, 0].set_ylim([0, 5])
    axis[1, 0].plot(x, modal_ch, linestyle='--', color='green', marker='o', label="The Proposed Model")
    axis[1, 0].plot(x, ema_ch, linestyle='--', color='purple', marker='x', label="EMA")
    axis[1, 0].plot(x, scpq_ch, linestyle='--', color='red', marker='v', label="SCPQ")
    axis[1, 0].grid()

    # Third graph Aversive Valence with bad outcome
    modal_vb = np.array([5 - 1.88370707071, 5 - 0.623830808081, 5 - 0.623830808081])  # questa è valenza positiva
    ema_vb = np.array([3.3, 4.4, 5])
    scpq_vb = np.array([2.57, 2.73, 2.79])

    y = np.array([0, 1, 2])
    yticks = np.array(['Start', 'Middle', 'Bad'])

    axis[2, 0].set_title('Aversive Valence')
    axis[2, 0].set_xticks(y)
    axis[2, 0].set_xticklabels(yticks)
    axis[2, 0].set_ylim([0, 5])
    axis[2, 0].plot(y, modal_vb, linestyle='--', color='green', marker='o', label="The Proposed Model")
    axis[2, 0].plot(y, ema_vb, linestyle='--', color='purple', marker='x', label="EMA")
    axis[2, 0].plot(y, scpq_vb, linestyle='--', color='red', marker='v', label="SCPQ")
    axis[2, 0].grid()

    # Third graph Aversive Valence with good outcome
    modal_vg = np.array([5 - 1.88370707071, 5 - 0.623830808081, 5 - 3.57196890547])  # questa è valenza positiva
    ema_vg = np.array([3.3, 4.2, 0])
    scpq_vg = np.array([2.57, 2.73, 1.08])

    y = np.array([0, 1, 2])
    yticks = np.array(['Start', 'Middle', 'Good'])

    axis[3, 0].set_title('Aversive Valence')
    axis[3, 0].set_xticks(y)
    axis[3, 0].set_xticklabels(yticks)
    axis[3, 0].set_ylim([0, 5])
    axis[3, 0].plot(y, modal_vg, linestyle='--', color='green', marker='o', label="The Proposed Model")
    axis[3, 0].plot(y, ema_vg, linestyle='--', color='purple', marker='x', label="EMA")
    axis[3, 0].plot(y, scpq_vg, linestyle='--', color='red', marker='v', label="SCPQ")
    axis[3, 0].grid()

    # First graph Loss Controllability
    modal_cl = np.array([1.04166666667, 0])
    ema_cl = np.array([0, 0])
    scpq_cl = np.array([2.57, 2.08])

    axis[0, 1].set_title('Loss Controllability')
    axis[0, 1].set_xticks(x)
    axis[0, 1].set_xticklabels(xticks)
    axis[0, 1].set_ylim([0, 5])
    axis[0, 1].plot(x, modal_cl, linestyle='--', color='green', marker='o', label="The Proposed Model")
    axis[0, 1].plot(x, ema_cl, linestyle='--', color='purple', marker='x', label="EMA")
    axis[0, 1].plot(x, scpq_cl, linestyle='--', color='red', marker='v', label="SCPQ")
    axis[0, 1].grid()

    # Second graph Loss Changeability
    modal_chl = np.array([0.833333333333, 0.416666666667])
    ema_chl = np.array([2.1, 1.2])
    scpq_chl = np.array([1.41, 1.12])

    axis[1, 1].set_title('Loss Changeability')
    axis[1, 1].set_xticks(x)
    axis[1, 1].set_xticklabels(xticks)
    axis[1, 1].set_ylim([0, 5])
    axis[1, 1].plot(x, modal_chl, linestyle='--', color='green', marker='o', label="The Proposed Model")
    axis[1, 1].plot(x, ema_chl, linestyle='--', color='purple', marker='x', label="EMA")
    axis[1, 1].plot(x, scpq_chl, linestyle='--', color='red', marker='v', label="SCPQ")
    axis[1, 1].grid()

    # Third graph Loss Valence with bad outcome
    modal_vbl = np.array(
        [5 - 1.45833333333, 5 - 0.625, 5 - 0.625])  # questa è valenza positiva
    ema_vbl = np.array([2, 3, 5])
    scpq_vbl = np.array([2.75, 2.65, 2.99])

    y = np.array([0, 1, 2])
    yticks = np.array(['Start', 'Middle', 'Bad'])

    axis[2, 1].set_title('Loss Valence')
    axis[2, 1].set_xticks(y)
    axis[2, 1].set_xticklabels(yticks)
    axis[2, 1].set_ylim([0, 5])
    axis[2, 1].plot(y, modal_vbl, linestyle='--', color='green', marker='o', label="The Proposed Model")
    axis[2, 1].plot(y, ema_vbl, linestyle='--', color='purple', marker='x', label="EMA")
    axis[2, 1].plot(y, scpq_vbl, linestyle='--', color='red', marker='v', label="SCPQ")
    axis[2, 1].grid()

    # Third graph Loss Valence with good outcome
    modal_vgl = np.array(
        [5 - 1.45833333333, 5 - 0.625, 5 - 3.73263888889])  # questa è valenza positiva
    ema_vgl = np.array([2, 3, 0])
    scpq_vgl = np.array([2.75, 2.65, 0.90])

    y = np.array([0, 1, 2])
    yticks = np.array(['Start', 'Middle', 'Good'])

    axis[3, 1].set_title('Loss Valence')
    axis[3, 1].set_xticks(y)
    axis[3, 1].set_xticklabels(yticks)
    axis[3, 1].set_ylim([0, 5])
    axis[3, 1].plot(y, modal_vgl, linestyle='--', color='green', marker='o', label="The Proposed Model")
    axis[3, 1].plot(y, ema_vgl, linestyle='--', color='purple', marker='x', label="EMA")
    axis[3, 1].plot(y, scpq_vgl, linestyle='--', color='red', marker='v', label="SCPQ")
    axis[3, 1].grid()

    # Combine all the operations and display
    plt.legend(bbox_to_anchor=(1.05, 0.3), loc='upper left')
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # plot_emotion()
    plot_appraisal()
    # plot_controllability()


