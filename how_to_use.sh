export YOUTUBE_API_KEY='AIzaSyCsUPblou69VljjTinksj3d5IgjJzjgbtY'

export API_ENDPOINT="https://youtube.googleapis.com/youtube/v3/playlistItems"
export PART="id,contentDetails,snippet,status"
export PLAYLIST_ID="UU1EB8moGYdkoZQfWHjh7Ivw"

curl "${API_ENDPOINT}?part=${PART}&playlistId=${PLAYLIST_ID}&key=${YOUTUBE_API_KEY}" | jq .



## channel: list
# peanuts kun
YOUTUBE_API_KEY='AIzaSyCsUPblou69VljjTinksj3d5IgjJzjgbtY'
PART="id,snippet,contentDetails"
CHANNEL_ID="UCmgWMQkenFc72QnYkdxdoKA"
curl "https://www.googleapis.com/youtube/v3/channels?part=${PART}&id=${CHANNEL_ID}&key=${YOUTUBE_API_KEY}" | jq .

> UUmgWMQkenFc72QnYkdxdoKA


# ponpoko
YOUTUBE_API_KEY='AIzaSyCsUPblou69VljjTinksj3d5IgjJzjgbtY'
PART="id,snippet,contentDetails"
CHANNEL_ID="UC1EB8moGYdkoZQfWHjh7Ivw"
curl "https://www.googleapis.com/youtube/v3/channels?part=${PART}&id=${CHANNEL_ID}&key=${YOUTUBE_API_KEY}" | jq .

> UU1EB8moGYdkoZQfWHjh7Ivw


## playlistItem: list

# peanuts
YOUTUBE_API_KEY='AIzaSyCsUPblou69VljjTinksj3d5IgjJzjgbtY'
PART="id,contentDetails,snippet,status"
PLAYLIST_ID="UUmgWMQkenFc72QnYkdxdoKA"
curl "https://www.googleapis.com/youtube/v3/playlistItems?part=${PART}&playlistId=${PLAYLIST_ID}&key=${YOUTUBE_API_KEY}" | jq .


## stats




### エントリー1: 第１話「#ハッシュタグ」オシャレになりたい！ピーナッツくん【自主制作アニメ】
https://www.youtube.com/watch?v=s-jGOeYdKt8



### エントリー2: ピーナッツくん -"VIRTUAFREAK -REWIRE-" Release live @渋谷clubasia
https://www.youtube.com/watch?v=_nXnvHit0R4



### エントリー3: ピーナッツくん 『 グミ超うめぇ 』Official Music Video / Album "False Memory Syndrome"
https://www.youtube.com/watch?v=9VhrJCbr58A

### エントリー4: 【MV】刀ピークリスマスのテーマソング2020 / ピーナッツくん
https://www.youtube.com/watch?v=BVC-dRCz-4A


### エントリー5: 今年もたくさんお世話になりました。
https://www.youtube.com/watch?v=b5VxEOiHvdY

### エントリー6: ぽんぽこVSピーナッツくん生活を賭けた大勝負。

https://www.youtube.com/watch?v=IgBtOvlj2X8

### エントリー7: ガチ恋ぽんぽこ、結婚します。
https://www.youtube.com/watch?v=n8msiA8RNxg

### エントリー8: ぽんぽこがピンチです。
https://www.youtube.com/watch?v=Kbfrw9yFGx0



cat output/video_json/peanuts_kun/video_list.json | jq '. | map(.videoID) | count'
cat output/video_json/ponpoko/video_list.json | jq '. | map(.videoID) | count'

cat output/video_json/peanuts_kun/video_list.json | jq '. | map(.videoID)' > tmp/peanuts_kun.json
cat output/video_json/ponpoko/video_list.json | jq '. | map(.videoID)' > tmp/ponpoko.json
cat tmp/peanuts_kun.json tmp/ponpoko.json | jq -s add | jq '. | unique | length'


for id in s-jGOeYdKt8 _nXnvHit0R4 9VhrJCbr58A BVC-dRCz-4A b5VxEOiHvdY IgBtOvlj2X8 n8msiA8RNxg Kbfrw9yFGx0
do
	cat output/pict_img/180x320/$id/pict_img.json | jq '. | flatten | unique' > ./tmp/$id.json
done

cat tmp/s-jGOeYdKt8.json tmp/_nXnvHit0R4.json tmp/9VhrJCbr58A.json tmp/BVC-dRCz-4A.json tmp/b5VxEOiHvdY.json tmp/IgBtOvlj2X8.json tmp/n8msiA8RNxg.json tmp/Kbfrw9yFGx0.json \
  | jq -s add \
  | jq '. | unique | length'

1206


all=`cat tmp/peanuts_kun.json tmp/ponpoko.json | jq -s add | jq '. | unique'`
used=`cat tmp/s-jGOeYdKt8.json tmp/_nXnvHit0R4.json tmp/9VhrJCbr58A.json tmp/BVC-dRCz-4A.json tmp/b5VxEOiHvdY.json tmp/IgBtOvlj2X8.json tmp/n8msiA8RNxg.json tmp/Kbfrw9yFGx0.json \
  | jq -s add \
  | jq '. | unique'`

echo -n "{\"all\": $all, \"used\": $used}" | jq '.all-.used | length'

echo -n "{\"all\": $all, \"used\": $used}" | jq '.all-.used'

(git)[main]
[
  "5TvCvoeRVqk",
  "686jx1MepsE",
  "8Ke-sFIM9hY",
  "BbGbA3nN4_s",
  "FipiU35xpUw",
  "GSMy65lxbT0",
  "M7nCXigtMt0",
  "Mf2oPz8LUGc",
  "OIQCM4iU2dA",
  "P66Apt5-v6A",
  "STme7z6pQ1g",
  "Ywj7o_h3ddg",
  "bbSaAekGdPQ",
  "eMbUvYqzXMQ",
  "fy8zXfE26P8",
  "jUaECEAdfXU",
  "rWgJAf5WxCM",
  "sMgTf15x3Xs",
  "wODnFp8_5Yc",
  "ycrnLS5Jk0c"
]



## comment search
export YOUTUBE_API_KEY='AIzaSyCsUPblou69VljjTinksj3d5IgjJzjgbtY'

export API_ENDPOINT="https://youtube.googleapis.com/youtube/v3/videos"
export PART="id,snippet"
export PLAYLIST_ID="UU1EB8moGYdkoZQfWHjh7Ivw"

curl "${API_ENDPOINT}?part=${PART}&playlistId=${PLAYLIST_ID}&key=${YOUTUBE_API_KEY}" | jq .
