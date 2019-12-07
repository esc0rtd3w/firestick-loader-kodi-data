"""
    urlresolver XBMC Addon
    Copyright (C) 2014 tknorris

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    reusable captcha methods
"""
import re
import xbmcgui
import xbmc
import os
import random

IMG_FILE = 'captcha_img.png'

google_nid = [
    '67=mwocoU0FoMG_dewxiEO3zDc7LLQtKVabiaezQsipcVb-020jysQ9qfngMTyIYNGsub8G7eQBqQPuTXUAO3GJVFZZWjF4tawOwj0KGaRTbw27z0ZEuZtSN-98hX1KedvpY_rzoHyd-InVhDtoG9dqONDS88RmP8JxgZAz7GhtH_QWpTk1WUIY4WTMb6AQ5f58oYUlgQ',
    '67=pLb98eXX7XshplSC25O1hUrM6VPe1bG9epaYJREF4EBGoV-TPIQ0MynwuZdb1ra4i_j8jfzeKgHyJRL917tqVvJ1drL2BTn2QE4HaRblzxd0lpITPiswWjYNWO3YMn8g0aV7bw3zFqdW9HrdT3h2iJxykpn7QTCJm7fFHZoSYVRR1zWL_jNpSHvs7u912M5K1skdqY-lGtU',
    '67=OxBGxDxcR3S52tk-887HgVRyFu9krkOitMKqvUrTaPH_R4ugfYUiCL0lqR2Rxm4aESGXngTHsAppfZb5Qdkf_e0v7RCu0Oq4d8z65ZJ9KMRrCXEfVBP0-iMOQxPeCWfY',
    '67=pKWLKXjRlCT2pQqthlZjlo2_mbcU2HYox1ApF-RwFLz6MCvuMsBSGOGh7yka3gcvrwx8aYta0Yvq_fPJor_nJT0gOO5vSPvDVIg__dZZoZ9DQXHO8VHqcd1aZPSXDS5v',
    '67=vbE1-owJvPDeppE4EZJC-8Z-_BvsBleEcsL7lTnrvwxeG4CczVK-fcH0Wx8O-ODFuB6lm4EKQ1TZ_3YXGtd3kWPGLmjdVjmCgAhp5gAmTxSOVXvVVOCGzKR8eL_TPeL_',
    '67=FaE2a-AnkczIWt5jMDccNY4V_PxBf966Z77a70AyS0aueqyp9T_rysO4G2npXwJbvOaoEOZzz9tWqHtA2883hFkuYuw4DkkNLnKFRm_XlS_CgnpMkCLTuqKj7b9vxI7U',
    '67=T3PTCfatBsA-IZ8VEBbAllJVn6JUuuwtpbJCTXb7lRS9eQ-VArRF4pJsmGhGOCMpUsbTaTfWhqS5e2DgCER6NnBU6FDAU7eT-TrkokJhhOReEMM7jU-540KtVEml6ILg',
    '67=Sg6vIy8i48EwAzU9XoN_-jbgt7Fmo2QHck9I_FlUlSDgwlRF2uTaxVpt6AQ5TNMsB9wQICFhS62NjV8A6vp3XNaqlPfflr5pfFtEQP92B5vjz9J6BFcjFzXQPdzEYjzf',
    '67=gmwkHvz9DPD4aAkvWASWLckCXt-Bk3I050ok3RJClKDauzHvsgdLPrIeeLWK641RII82H42Ft5FECeKESQhscza18dzAKP0MJXQW6KDOQ6YGs5RA6kJrQrxPcGmyFvYy',
    '67=ZAQc_dn0FqYZ1d94-kUyiuy2z8wbPFzBps0JQ5uvezEdZEXpDKorCAGwLtS-byDcuO4rH2fLSjgjDEb9g8uBD4uteRfFbIBE8KwmrJWnhAjvW6wAun4He9sWvQREyTcJ',
    '67=ZAlxN3yhjTrFufC58FtofKUgd1EpBDH5V5KhdNoim_yGDDTMyyhvLdhYEevm84-Wg66zeHwGdnaFMzr_og0yJgjsNTpFeKo872exiCknsH4Nd1PRbm33Aa9W8oK-WBDa',
    '67=ZAlxN3yhjTrFufC58FtofKUgd1EpBDH5V5KhdNoim_yGDDTMyyhvLdhYEevm84-Wg66zeHwGdnaFMzr_og0yJgjsNTpFeKo872exiCknsH4Nd1PRbm33Aa9W8oK-WBDa',
    '67=s5Du4EheeC4qgE8wCp1UpOV-qVFHLeRblrMBRtbsvSf_FJzu5HF6ukgcUx4l_g74TcqLJtS40PNxLB_qyxnCAoMw5VJ2A6pdYyZeco1cYfP35EjWDjCIpk0DdlQCkuhB',
    '67=KhPqWmMY01FJyf4kUyk5DhP8RMb9rh3qCjIOu2AGlOrrGB6QqPHpAkcWj3W9um0nNVx2EMzw2RFjbWtZMAI1PajDJUvoM0fnq_OdqdR7NziPOuq6ofWcmjTMFr0mouW3',
    '67=EodF-df4x5VWS1nN4U9P9tVy3UZ-h7_P4098hgcal9Hggmou_FqN-0NW2u0IeP28k6xal-Wr4VNtGGn4PJqEHCTUDmMiCbeSDJiJPhnIi9wcjk8yMUQ9muf3JcS_5Aqz',
    '67=m9-42qMKY6sRGB-KSRsiFYfjsijMBZqa_w5DJnXmT3x2c2IOBVv6IezuvZ-CX9wqAvyeFJ_VXkF9FDMuC1bDSYlt0rnxiYbIWQJsfMTG1cGLoFKfK-QYhPkLgAo0Ybxi',
    '67=AbA52z04VG54UFjWoUiGTCSSH1dmRdBH5l84_ZtGEEwqPOH0AmZuqZMIlgzI8JyhBdDVrd8Hu5sanWxre-JnGkARQEBq9h0E3OblL_ZArLQWXJcYy8Ui6ETUkRZxTiOK',
    '67=Tom5nqBLRUGu4hO74mEMmLVjKfCebyXSuQYH3CbmRViCm8nKZVBWzs0_r94SRwh-hTUqXfnnCSFVg2fqG2N9X6HOncsDjOLIek4Bo0PxCvXiuVsGuP_XmJvdumr8jAmM',
    '67=QjGKq3LTgjo1vC0W-aTz0Nor4Jm3X_ecn7VGszvQH7hY-XqFK6wflSJHLcUPY0kDc12XNEW_CrHAcXM0W36xICEpUBrVFH6DtHIcKS1O5aeXt-jA-T8BnZoI34c2BhVa',
    '67=DFIOnS1Nr3N6y0YE3Qx-CaaHYVlWyV10GIJTtIFQ-6_iZGNjtrimgPWlWPX5-zMLf9R76-Xyi5m4kZ0_9KMGChnZKTYTmEAZqHwAV-Q1p5Bc9PyVf-Lt5kO0EuxEAq5x',
    '67=hW7zo2M6vOcFnwq4vvUloeE8NxM5n6L_jbJocYSA0yirrh4QTviVmvqcLOW2WM4KjJGLi01xIa9O0PrhWaPqKBtP_hz1wINF2nW7trMfR0T2aXyEDoNuDNeUUXAAjIhB',
    '67=qAT-ji1lswEweR4BMbdLhdZHczj54O6s-OSFgH_rcjXLpOtjej9OR8ADiptMVjARY1hTWPadfixc3lZkfX41XuLFKK_B2J-hsEFHEdxkiL2IAW_AUyZ1MDYUs-Z8_l8q',
    '67=pjyblxE4achNlGvw7LXzPoBVuEBq-VekSZSnd8isuMSgCEvV52szci3mISZH1vxvwFIFFoJQhNROOfwP7HhfLSXaPcIRBC44c19BNcxQn1bNTNTKRCNK8US9LQ1ksMPH',
    '67=ZI_Eq9CM_PwpYyXE4x__N50BT1lySFyYw62MgeJorqhs7QYHw2X4kJVi2C5QocansHBQGXIEBIAxFxS9qlTLQp2KIYoVd4SBBYT6lE0CNtPZdA5EnrPoTev6pwqu06n4']

def get_response(img):
    try:
        img = xbmcgui.ControlImage(450, 0, 400, 130, img)
        wdlg = xbmcgui.WindowDialog()
        wdlg.addControl(img)
        wdlg.show()
        xbmc.sleep(3000)
        kb = xbmc.Keyboard('', 'Type the letters in the image', False)
        kb.doModal()
        if (kb.isConfirmed()):
            solution = kb.getText()
            if solution == '':
                raise Exception('You must enter text in the image to access video')
            else:
                return solution
        else:
            raise Exception('Captcha Error')
    finally:
        wdlg.close()

def do_captcha(html):
    solvemedia = re.search('<iframe src="((?:https?:)?//api.solvemedia.com[^"]+)', html)
    recaptcha = re.search('<script\s+type="text/javascript"\s+src="(http://www.google.com[^"]+)', html)
    xfilecaptcha = re.search('<img\s+src="([^"]+/captchas/[^"]+)', html)
    
    if solvemedia:
        return do_solvemedia_captcha(solvemedia.group(1))
    elif recaptcha:
        print('yes')
        return do_recaptcha(recaptcha.group(1))
    elif xfilecaptcha:
        return do_xfilecaptcha(xfilecaptcha.group(1))
    else:
        captcha = re.compile("left:(\d+)px;padding-top:\d+px;'>&#(.+?);<").findall(html)
        result = sorted(captcha, key=lambda ltr: int(ltr[0]))
        solution = ''.join(str(int(num[1]) - 48) for num in result)
        if solution:
            return {'code': solution}
        else:
            return {}

def do_solvemedia_captcha(captcha_url):
    if captcha_url.startswith('//'): captcha_url = 'http:' + captcha_url
    html = client.request(captcha_url)
    data = {
            'adcopy_challenge': ''  # set to blank just in case not found; avoids exception on return
    }
    for match in re.finditer(r'type=hidden.*?name="([^"]+)".*?value="([^"]+)', html):
        name, value = match.groups()
        data[name] = value

    captcha_img = os.path.join(common.profile_path, IMG_FILE)
    try: os.remove(captcha_img)
    except: pass
    
    #Check for alternate puzzle type - stored in a div
    alt_frame = re.search('<div><iframe src="(/papi/media[^"]+)', html)
    if alt_frame:
        html = client.request("http://api.solvemedia.com%s" % alt_frame.group(1))
        alt_puzzle = re.search('<div\s+id="typein">\s*<img\s+src="data:image/png;base64,([^"]+)', html, re.DOTALL)
        if alt_puzzle:
            open(captcha_img, 'wb').write(alt_puzzle.group(1).decode('base64'))
    else:
        open(captcha_img, 'wb').write(net.http_GET("http://api.solvemedia.com%s" % re.search('<img src="(/papi/media[^"]+)"', html).group(1)).content)
            
    solution = get_response(captcha_img)
    data['adcopy_response'] = solution
    html = client.request('http://api.solvemedia.com/papi/verify.noscript', post=data)
    return {'adcopy_challenge': data['adcopy_challenge'], 'adcopy_response': 'manual_challenge'}

def do_recaptcha(captcha_url):
    if captcha_url.startswith('//'): captcha_url = 'http:' + captcha_url
    captcha_nid = 'NID=' + random.choice(google_nid)
    headers = {'Cookie': captcha_nid}
    html = client.request(captcha_url, headers=headers)
    part = re.search("challenge \: \\'(.+?)\\'", html)
    captcha_img = 'http://www.google.com/recaptcha/api/image?c=' + part.group(1)
    solution = get_response(captcha_img)
    return {'recaptcha_challenge_field': part.group(1), 'recaptcha_response_field': solution}

def do_xfilecaptcha(captcha_url):
    if captcha_url.startswith('//'): captcha_url = 'http:' + captcha_url
    solution = get_response(captcha_url)
    return {'code': solution}
