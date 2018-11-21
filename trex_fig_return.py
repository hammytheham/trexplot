# coding: utf-8

import trexplot as tp

def main():
    plots=tp.main()
    print(plots)
    fig,ax=plots['fig_TopPorositypcolor']
    ax.set_title('Power of da python')
    ax.set_xlabel('Total Sauce')
    ax.set_xlim(300,500)
    ax.set_ylim(200,800)
    fig.show()

if __name__ == "__main__":
    main()
