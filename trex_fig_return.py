# coding: utf-8

import trexplot as tp

def main():
    plots=tp.main()
    print(plots)
#    fig,ax=plots['fig_TopPerm_X(m2)pcolor']
#    fig,ax=plots['fig_TopTemperature(C)pcolor']
    fig,ax=plots['fig_xsec_y_halfTemperature(C)pcolor']
#
    ax.set_title('Power of da python')
    ax.set_xlabel('Total Sauce')
#    ax.set_xlim(300,500)
#    ax.set_ylim(200,800)
    fig.savefig('/Users/hamish/Desktop/TREXWORK/testfig')
#    fig.show()
if __name__ == "__main__":
    main()
