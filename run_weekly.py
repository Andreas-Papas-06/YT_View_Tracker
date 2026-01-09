from sheets_updating.yt_read import get_video_input
from sheets_updating.get_yt_views import get_views
from sheets_updating.update_sumaries import update_sum



def main():
    get_video_input()
    get_views()
    update_sum()



if __name__ == '__main__':
    main()