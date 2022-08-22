emoji_dict = {u'👭': u'🌈', u'👬': u'🌈', u'😃': u'😀', u'😄': u'😀',
              u'😁': u'😀', u'😆': u'😀', u'😅': u'😀', u'😂': u'😀',
              u'🤣': u'😀', u'😊': u'😀', u'😇': u'😀', u'🙂': u'😀',
              u'🙃': u'😀', u'😉': u'😀', u'😌': u'😀', u'😺': u'😀',
              u'😸': u'😀', u'😹': u'😀', u'😘': u'😍', u'😗': u'😍',
              u'😙': u'😍', u'😚': u'😍', u'😋': u'😍', u'🤗': u'😍',
              u'😻': u'😍', u'💋': u'😍', u'💛': u'😍', u'💚': u'😍',
              u'💙': u'😍', u'💜': u'😍', u'🖤': u'😍', u'💕': u'😍',
              u'💞': u'😍', u'💓': u'😍', u'💗': u'😍', u'💖': u'😍',
              u'💝': u'😍', u'😽': u'😍', u'😏': u'😔', u'😒': u'😔',
              u'😞': u'😔', u'😟': u'😔', u'😕': u'😔', u'🙁': u'😔',
              u'😣': u'😔', u'😖': u'😔', u'😩': u'😔', u'😢': u'😔',
              u'😭': u'😔', u'😿': u'😔', u'💔': u'😔', u'😤': u'😡',
              u'😠': u'😡', u'😬': u'😡', u'😾': u'😡', u'😶': u'😐',
              u'😑': u'😐', u'😯': u'😳', u'😦': u'😳', u'😧': u'😳',
              u'😮': u'😳', u'😲': u'😳', u'😵': u'😳', u'😨': u'😱',
              u'🙀': u'😱', u'😥': u'😓', u'😪': u'😓', u'🙄': u'🤔',
              u'💩': u'🤢', u'😝': u'😜', u'😛': u'😜', u'😈': u'👹',
              u'👿': u'👹', u'👺': u'👹', u'🤘': u'👹', u'🤙': u'👹',
              u'🤧': u'🤒', u'😷': u'🤒', u'🤕': u'🤒', u'👻': u'💀',
              u'👽': u'💀', u'👌': u'👍', u'🤚': u'🙏', u'💐': u'🙏',
              u'🌷': u'🙏', u'🌹': u'🙏', u'🌻': u'🙏', u'🌼': u'🙏',
              u'🌸': u'🙏', u'🌺': u'🙏', u'🙌': u'🤝', u'👊': u'👎',
              u'👉': u'👆', u'👇': u'👆', u'👈': u'👆', u'💦': u'👙',
              u'🔞': u'👙', u'🙊': u'🙈', u'☺': u'😀', u'❤': u'😍',
              u'❣': u'😍', u'☹': u'😔', u'☠': u'💀', u'✋': u'🙏',
              u'☝': u'👆', u'♐': u'👙'}

rain_symbols = {u'👨‍👨‍👧‍👦', u'👨‍👨‍👦‍👦', u'👨‍👨‍👧‍👧', u'👩‍👩‍👧‍👦',
                u'👩‍👩‍👦‍👦', u'👩‍👩‍👧‍👧', u'👨‍❤️‍💋‍👨', u'👩‍❤️‍💋‍👩',
                u'👩‍👩‍👦', u'👩‍👩‍👧', u'👨‍👨‍👦', u'👨‍👨‍👧', u'👨‍❤️‍👨',
                u'👩‍❤️‍👩'}

allowed_persian_chars = '\u0627\u0628\u062A\u062B\u062C\u062D' \
                        '\u062E\u062F\u0630\u0631\u0632\u0633\u0634\u0635' \
                        '\u0636\u0637\u0638\u0639\u063A\u0641\u0642\u06A9' \
                        '\u0644\u0645\u0646\u0647\u0648\u067E\u0686\u0698' \
                        '\u06AF\u06CC\u0622'

allowed_halfspace_chars = '\u200B\u200C\u200D\u200E\u200F\u00AC'

english_alphabet = 'abcdefghijklmnopqrstuvwxyzğıöüşç' \
                   'ABCDEFGHIJKLMNOPQRSTUVWXYZĞİÖÜŞÇ0123456789'

english_marker = '\u0021\u0022\u0025\u0026\u0027\u0028' \
                 '\u0029\u002A\u002B\u002C\u002D\u002E\u002F' \
                 '\u003A\u003B\u003C\u003D\u003E\u003F\u0040\u005B' \
                 '\u005C\u005D\u005E\u005F\u0060\u007B\u007C\u007D' \
                 '\u007E\u00AB\u00BB\u066C\u061F\u00F7\u00B7\u00A1' \
                 '\u00A2\u00B0\u00B1\u00B4\u00A6\u061F\uFF1A\u00BF' \
                 '\u060C\u061B\u00D7'

exception_marker = '?!'
set_english_marker = set(english_marker).difference(set(exception_marker))

currency_symbols = '$€¥£₣₺₽₠₡₢₤₥₦₧₨₩₪₫₭₮₯₰₱₲₳₴₵₶₷₸₹₻₼₾₿'

selected_emojies = '🌈😀😍😔😡😐😳😱😓🤔🤢😜👹🤒💀👍🙏🤝👎👆👙🙈'

allowed_pass_chars = '\u064B\u064C\u064D\u064E\u064F\u0650\u0651' \
                     '\u0652\u0653\u0654\u0655\u0656\u0657\u0658\u0659' \
                     '\u065A\u065B\u065D\u065E\u065F\u0618\u0619\u061A' \
                     '\u0670\u00B0\u0674\uFE7E\u06DA\u06D6\u0060\u0640'

reformation_alphabet_dict = {
    u'\u0660': u'0', u'\u0661': u'1', u'\u0662': u'2', u'\u0663': u'3',
    u'\u0664': u'4', u'\u0665': u'5', u'\u0666': u'6', u'\u0667': u'7',
    u'\u0668': u'8', u'\u0669': u'9', u'\u06F0': u'0', u'\u06F1': u'1',
    u'\u06F2': u'2', u'\u06F3': u'3', u'\u06F4': u'4', u'\u06F5': u'5',
    u'\u06F6': u'6', u'\u06F7': u'7', u'\u06F8': u'8', u'\u06F9': u'9',
    u'\u0643': u'ک', u'\u063B': u'ک', u'\u063C': u'ک', u'\u06AA': u'ک',
    u'\u06AB': u'ک', u'\u06AC': u'ک', u'\u06AD': u'ک', u'\u06AE': u'ک',
    u'\u0762': u'ک', u'\u0763': u'ک', u'\u0764': u'ک', u'\u077F': u'ک',
    u'\u08B4': u'ک', u'\u0620': u'ی', u'\u0649': u'ی', u'\u064A': u'ی',
    u'\u0626': u'ی', u'\u063D': u'ی', u'\u063E': u'ی', u'\u063F': u'ی',
    u'\u0678': u'ی', u'\u06CD': u'ی', u'\u06CE': u'ی', u'\u06D0': u'ی',
    u'\u06D1': u'ی', u'\u06D2': u'ی', u'\u06D3': u'ی', u'\u08A8': u'ی',
    u'\u08A9': u'ی', u'\u06D5': u'ه', u'\u06C0': u'ه', u'\u06BE': u'ه',
    u'\u06C1': u'ه', u'\u0624': u'و', u'\u0623': u'ا', u'\u0625': u'ا',
    u'\u0629': u'ه', u'\uFE8E': u'ا', u'\uFE8D': u'ا',
    u'\uFEA9': u'د', u'\uFEAE': u'ر', u'\uFE91': u'ب', u'\uFEAD': u'ر',
    u'\u067A': u'ت', u'\uFEE3': u'م', u'\uFEAA': u'د', u'\uFEEA': u'ه',
    u'\uFEEE': u'و', u'\uFEE7': u'ن', u'\uFEED': u'و', u'\uFBFF': u'ی',
    u'\uFBFE': u'ی', u'\uFBFD': u'ی', u'\uFEE8': u'ن', u'\uFEB3': u'س',
    u'\uFEEB': u'ه', u'\uFEE5': u'ن', u'\uFEAF': u'ز', u'\uFE96': u'ت',
    u'\uFEB7': u'ش', u'\uFB90': u'ک', u'\uFE98': u'ت', u'\uFEE4': u'م',
    u'\uFE97': u'ت', u'\uFEA7': u'خ', u'\uFBFC': u'ی', u'\uFEE6': u'ن',
    u'\uFEE2': u'م', u'\uFEE9': u'ه', u'\uFEB4': u'س', u'\uFB94': u'گ',
    u'\uFECB': u'ع', u'\uFEB8': u'ش', u'\uFEDF': u'ل', u'\uFE81': u'ا',
    u'\uFED3': u'ف', u'\uFEE1': u'م', u'\uFE92': u'ب', u'\uFEE0': u'ل',
    u'\uFEA3': u'ح', u'\uFEF4': u'ی', u'\uFB95': u'گ', u'\uFB58': u'پ',
    u'\uFEEC': u'ه', u'\u06B9': u'ن', u'\uFE9F': u'ج', u'\uFB7C': u'چ',
    u'\uFED7': u'ق', u'\uFB91': u'ک', u'\uFEF3': u'ی', u'\uFEB0': u'ز',
    u'\uFED8': u'ق', u'\uFECC': u'ع', u'\uFED4': u'ف', u'\uFEDD': u'ل',
    u'\uFE95': u'ت', u'\uFEDB': u'ک', u'\uFEA8': u'خ', u'\uFEA0': u'ج',
    u'\uFEDE': u'ل', u'\uFEB6': u'ش', u'\uFEFC': u'لا', u'\uFEB5': u'ش',
    u'\uFE8F': u'ب', u'\u0671': u'ا', u'\u0769': u'ن', u'\uFB8F': u'ک',
    u'\uFEBB': u'ص', u'\uFEF2': u'ی', u'\u060F': u'ع', u'\uFEA4': u'ح',
    u'\uFEF0': u'ی', u'\u0767': u'ن', u'\uFECF': u'غ', u'\uFE90': u'ب',
    u'\uFEC4': u'ط', u'\uFEC3': u'ط', u'\uFED6': u'ق', u'\uFEB2': u'س',
    u'\uFEFB': u'لا', u'\uFEAC': u'ذ', u'\uFEBC': u'ص', u'\u06C2': u'ه',
    u'\uFEB1': u'س', u'\u06B8': u'ل', u'\uFEDC': u'ک', u'\uFB7D': u'چ',
    u'\uFEC0': u'ض', u'\uFEF1': u'ی', u'\uFB93': u'گ', u'\uFEC8': u'ظ',
    u'\uFED2': u'ف', u'\uFEEF': u'ی', u'\uFE8B': u'ی', u'\u076A': u'ل',
    u'\uFED5': u'ق', u'\uFEC2': u'ط', u'\uFBA9': u'ه', u'\u06BA': u'ن',
    u'\uFEBF': u'ض', u'\u08AA': u'ر', u'\uFED1': u'ف', u'\uFED0': u'غ',
    u'\uFB8E': u'ک', u'\uFB59': u'پ', u'\uFB7B': u'چ', u'\u06C6': u'و',
    u'\uFECA': u'ع', u'\u06C5': u'و', u'\u06B1': u'گ', u'\uFE9D': u'ج',
    u'\uFE9C': u'ث', u'\uFEAB': u'ذ', u'\u0672': u'ا', u'\uFB92': u'گ',
    u'\uFEC7': u'ظ', u'\u067C': u'ت', u'\uFB8B': u'ژ', u'\uFE9E': u'ج',
    u'\u0691': u'ر', u'\uFEDA': u'ک', u'\uFECD': u'غ', u'\uFEC9': u'ع',
    u'\u06C3': u'ه', u'\uFEA2': u'ح', u'\u0753': u'ت', u'\u06B5': u'ل',
    u'\uFEB9': u'ص', u'\uFDFC': u' ریال ', u'\uFE83': u'ا', u'\uFE8C': u'ی',
    u'\uFEA1': u'ح', u'\uFEA6': u'خ', u'\uFEC1': u'ط', u'\uFE84': u'ا',
    u'\uFEBD': u'ض', u'\u0675': u'ا', u'\uFE9A': u'ث', u'\uFBA7': u'ه',
    u'\uFE94': u'ه', u'\u0695': u'ر', u'\u0673': u'ا', u'\uFBAF': u'ی',
    u'\uFE86': u'و', u'\uFB8A': u'ژ', u'\u0766': u'م', u'\uFEBE': u'ض',
    u'\uFEA5': u'خ', u'\u0676': u'و', u'\uFED9': u'ک', u'\uFE87': u'ا',
    u'\uFEBA': u'ص', u'\u06FF': u'ه', u'\uFEC6': u'ظ', u'\u0765': u'م',
    u'\uFE93': u'ه', u'\u06FB': u'ض', u'\u0694': u'ر', u'\uFEF7': u'لا',
    u'\u06C7': u'و', u'\u06FA': u'ش', u'\u06FE': u'م', u'\uFB7A': u'چ',
    u'\uFECE': u'غ', u'\u06B6': u'ل', u'\uFBAE': u'ی', u'\u06BC': u'ن',
    u'\uFBA5': u'ه', u'\u06CF': u'و', u'\uFE85': u'و', u'\uFBA4': u'ه',
    u'\uFEC5': u'ظ', u'\uFBAC': u'ه', u'\uFE9B': u'ث', u'\u200B': u'\u200C',
    u'\u200D': u'\u200C', u'\u200E': u'\u200C', u'\u200F': u'\u200C',
    u'\u00AC': u'\u200C',
    u'\uFDFD': u' بسم الله الرحمن الرحیم ', u'\uFDFA': u' صلی الله علیه و سلم ',
    u'\uFDF2': u' الله ', u'\uFDFB': u' جل جلاله ', u'\u06CA': u'و'
}

sign_dict = {u'❕': u'!', u'¡': u'!', u'‼': u'!', u'⁉': u'!?', u'❓': u'?',
             u'❔': u'?', u'¿': u'?', '؟': u'?', '٪': u'%', '：': u':',
             '·': u'.', '»': u')', '«': u'(', '،': u',', '؛': u';',
             '﴾': u')', '﴿': u'('}

upper2lower = {
    u'\u0041': u'\u0061', u'\u0042': u'\u0062', u'\u0043': u'\u0063',
    u'\u0044': u'\u0064', u'\u0045': u'\u0065', u'\u0046': u'\u0066',
    u'\u0047': u'\u0067', u'\u0048': u'\u0068', u'\u0049': u'\u0069',
    u'\u004A': u'\u006A', u'\u004B': u'\u006B', u'\u004C': u'\u006C',
    u'\u004D': u'\u006D', u'\u004E': u'\u006E', u'\u004F': u'\u006F',
    u'\u0050': u'\u0070', u'\u0051': u'\u0071', u'\u0052': u'\u0072',
    u'\u0053': u'\u0073', u'\u0054': u'\u0074', u'\u0055': u'\u0075',
    u'\u0056': u'\u0076', u'\u0057': u'\u0077', u'\u0058': u'\u0078',
    u'\u0059': u'\u0079', u'\u005A': u'\u007A', u'\u011f': u'\u011e',
    u'\u0131': u'\u0130', u'\u00f6': u'\u00d6', u'\u00fc': u'\u00dc',
    u'\u015f': u'\u015e', u'\u00e7': u'\u00c7'
}

regex_duplicate = r'(.)\1{2,}'

link_specifiers = ['http', '.com', 'www', '.org', '.ir', '.net', '.info',
                   '.edu', '.gov', '.int']
