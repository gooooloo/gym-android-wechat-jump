class XiaomiMix2S:

    COOR_X_RESET = 500
    # this one is tricky: sometimes there is ad, so the button position is moved. I have to choose a coordinate covers
    # both cases.
    COOR_Y_RESET = 1626
    COOR_X_SWIPE = 500
    COOR_Y_SWIPE = 500

    PNG_ON_PHONE = '/data/local/tmp/test.png'
    PNG_ON_PC = '/tmp/wechat_jump_env.png'

    SCORE_DIGIT_WIDTH = 69
    SCORE_DIGIT_HEIGHT = 85
    SCORE_DIGIT_TOP = 324
    SCORE_DIGIT_LEFT_1 = 123
    SCORE_DIGIT_LEFT_2 = 203
    SCORE_COLOR_TARGET = 72

    MAX_WAIT_SECONDS_AFTER_JUMP = 5
    SLEEP_SECONDS_AFTER_RESET = 0.4

    STATE_AREA_TOP = 830
    STATE_AREA_BOTTOM = 1511

    # For those pixels with color between [LOW, HIGH], we think them as background
    BG_COLOR_BGR_LOW = (195, 190, 227)
    BG_COLOR_BGR_HIGH = (227, 235, 252)

    FOOT_COLOR = (102, 59, 55)


cfg = XiaomiMix2S


