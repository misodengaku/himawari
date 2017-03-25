# coding=utf-8
from django.db import models

class BroadcastStationModel(models.Model):

    class Meta:
        verbose_name = verbose_name_plural = "放送局"

    station_id = models.CharField("局ID", max_length=16, primary_key=True)
    name = models.CharField("局名", max_length=64)
    service_id = models.IntegerField("サービスID")
    transport_stream_id = models.IntegerField("トランスポートストリームID")
    original_network_id = models.IntegerField("オリジナルネットワークID")

    def __str__(self):
        return self.name

    def natural_key(self):
        return self.station_id


class ChannelModel(models.Model):

    class Meta:
        verbose_name = verbose_name_plural = "チャンネル"

    logical_channels = models.ManyToManyField('BroadcastStationModel', verbose_name='論理チャンネル')
    physical_channel = models.IntegerField('物理チャンネル')


class ProgramModel(models.Model):

    class Meta:
        verbose_name = verbose_name_plural = "番組"
        unique_together = (("event_id", "station", "title"))

    event_id = models.IntegerField("イベントID")
    station = models.ForeignKey('BroadcastStationModel', verbose_name='論理チャンネル')
    title = models.TextField("番組名")
    detail = models.TextField("番組内容", blank=True, null=True)
    start_time = models.DateTimeField("開始時刻")
    end_time = models.DateTimeField("終了時刻")
    categories = models.ManyToManyField('SubCategoryModel')

    def __str__(self):
        return "%d - %s" % (self.event_id, self.title)


class CategoryModel(models.Model):

    class Meta:
        verbose_name = verbose_name_plural = "番組カテゴリ"

    LARGE_CATEGORY_CHOICES = (
        (0x0, 'ニュース／報道'),
        (0x1, 'スポーツ'),
        (0x2, '情報／ワイドショー'),
        (0x3, 'ドラマ'),
        (0x4, '音楽'),
        (0x5, 'バラエティ'),
        (0x6, '映画'),
        (0x7, 'アニメ／特撮'),
        (0x8, 'ドキュメンタリー／教養'),
        (0x9, '劇場／公演'),
        (0xA, '趣味／教育'),
        (0xB, '福祉'),
        (0xC, '予備'),
        (0xD, '予備'),
        (0xE, '拡張'),
        (0xF, 'その他'),
    )
    category_id = models.IntegerField(
        "カテゴリ", choices=LARGE_CATEGORY_CHOICES, unique=True, primary_key=True)
    name = models.CharField("カテゴリ名", max_length=64)

    def get_name(self):
        return self.LARGE_CATEGORY_CHOICES[self.category_id][1]

    def __str__(self):
        return self.get_name()


class SubCategoryModel(models.Model):

    class Meta:
        verbose_name = verbose_name_plural = "番組サブカテゴリ"

    MIDDLE_CATEGORY_TABLE = {
        0: {
            0x0: '定時・総合',
            0x1: '天気',
            0x2: '特集・ドキュメント',
            0x3: '政治・国会',
            0x4: '経済・市況',
            0x5: '海外・国際',
            0x6: '解説',
            0x7: '討論・会談',
            0x8: '報道特番',
            0x9: 'ローカル・地域',
            0xA: '交通',
            0xF: 'その他',
        },
        1: {
            0x0: 'スポーツニュース',
            0x1: '野球',
            0x2: 'サッカー',
            0x3: 'ゴルフ',
            0x4: 'その他の球技',
            0x5: '相撲・格闘技',
            0x6: 'オリンピック・国際大会',
            0x7: 'マラソン・陸上・水泳',
            0x8: 'モータースポーツ',
            0x9: 'マリン・ウィンタースポーツ',
            0xA: '競馬・公営競技',
            0xF: 'その他',
        },
        2: {
            0x0: '芸能・ワイドショー',
            0x1: 'ファッション',
            0x2: '暮らし・住まい',
            0x3: '健康・医療',
            0x4: 'ショッピング・通販',
            0x5: 'グルメ・料理',
            0x6: 'イベント',
            0x7: '番組紹介・お知らせ',
            0xF: 'その他',
        },
        3: {
            0x0: '国内ドラマ',
            0x1: '海外ドラマ',
            0x2: '時代劇',
            0xF: 'その他',
        },
        4: {
            0x0: '国内ロック・ポップス',
            0x1: '海外ロック・ポップス',
            0x2: 'クラシック・オペラ',
            0x3: 'ジャズ・フュージョン',
            0x4: '歌謡曲・演歌',
            0x5: 'ライブ・コンサート',
            0x6: 'ランキング・リクエスト',
            0x7: 'カラオケ・のど自慢',
            0x8: '民謡・邦楽',
            0x9: '童謡・キッズ',
            0xA: '民族音楽・ワールドミュージック',
            0xF: 'その他',
        },
        5: {
            0x0: 'クイズ',
            0x1: 'ゲーム',
            0x2: 'トークバラエティ',
            0x3: 'お笑い・コメディ',
            0x4: '音楽バラエティ',
            0x5: '旅バラエティ',
            0x6: '料理バラエティ',
            0xF: 'その他',
        },
        6: {
            0x0: '洋画',
            0x1: '邦画',
            0x2: 'アニメ',
            0xF: 'その他',
        },
        7: {
            0x0: '国内アニメ',
            0x1: '海外アニメ',
            0x2: '特撮',
            0xF: 'その他',
        },
        8: {
            0x0: '社会・時事',
            0x1: '歴史・紀行',
            0x2: '自然・動物・環境',
            0x3: '宇宙・科学・医学',
            0x4: 'カルチャー・伝統文化',
            0x5: '文学・文芸',
            0x6: 'スポーツ',
            0x7: 'ドキュメンタリー全般',
            0x8: 'インタビュー・討論',
            0xF: 'その他',
        },
        9: {
            0x0: '現代劇・新劇',
            0x1: 'ミュージカル',
            0x2: 'ダンス・バレエ',
            0x3: '落語・演芸',
            0x4: '歌舞伎・古典',
            0xF: 'その他',
        },
        10: {
            0x0: '旅・釣り・アウトドア',
            0x1: '園芸・ペット・手芸',
            0x2: '音楽・美術・工芸',
            0x3: '囲碁・将棋',
            0x4: '麻雀・パチンコ',
            0x5: '車・オートバイ',
            0x6: 'コンピュータ・ＴＶゲーム',
            0x7: '会話・語学',
            0x8: '幼児・小学生',
            0x9: '中学生・高校生',
            0xA: '大学生・受験',
            0xB: '生涯教育・資格',
            0xC: '教育問題',
            0xF: 'その他',
        },
        11: {
            0x0: '高齢者',
            0x1: '障害者',
            0x2: '社会福祉',
            0x3: 'ボランティア',
            0x4: '手話',
            0x5: '文字（字幕）',
            0x6: '音声解説',
            0xF: 'その他',
        },
        14: {
            0x0: 'BS/地上デジタル放送用番組付属情報',
            0x1: '広帯域 CS デジタル放送用拡張',
            0x3: 'サーバー型番組付属情報',
            0x4: 'IP 放送用番組付属情報',
        },
        15: {
            0xF: 'その他',
        }
    }

    large_category = models.ForeignKey(CategoryModel, verbose_name="親カテゴリ")
    category_id = models.IntegerField("サブカテゴリID")
    name = models.CharField("サブカテゴリ名", max_length=64)

    def get_fullname(self):
        return self.__str__()

    def get_name(self):
        return self.MIDDLE_CATEGORY_TABLE[self.large_category.category_id][self.category_id]

    def __str__(self):
        return "%s - %s" % (
            self.large_category.get_name(),
            self.get_name())


class ScheduleModel(models.Model):

    class Meta:
        verbose_name = verbose_name_plural = "録画予約"

    program = models.ForeignKey(ProgramModel, verbose_name="番組")
    agent = models.CharField("録画を実行するエージェント", max_length=64)
