declare -a arr=(\
"anindilyakwa" \
"arrernte" \
"awabakal" \
"barunggam" \
"bigambul" \
"birpai" \
"boonwurrung" \
"brabralung" \
"bundjalung" \
"darkinyung" \
"dharawal" \
"dharug" \
"dhauwurd-wurrung" \
"dhurga" \
"eora" \
"gamilaraay-gamilaroi-kamilaroi" \
"githabul" \
"gumbaynggir" \
"gundungurra" \
"gunggay" \
"gureng-gureng" \
"jagara" \
"kaurna" \
"ku-ring-gai-gameraigal-0" \
"kungkari" \
"larrakia-laragiya-gulumirrgin" \
"meriam-mir" \
"muruwari" \
"narungga" \
"nganyaywana" \
"ngarigu" \
"nguri" \
"paakantyi" \
"palawa-karni-tasmanian-languages" \
"wadi-wadi" \
"wangkumara" \
"warray" \
"wiilman" \
"wiradjuri-0" \
"wiriyaraay" \
"wolyamidi" \
"wonnarua" \
"worimi" \
"wulwulam" \
"wuna" \
"yuwaalaraay-euahlayi-yuwaaliyaay")

for i in "${arr[@]}"
do
   echo "$i"
   curl "http://indigenous.sl.nsw.gov.au/communities/$i" -o "$i.txt"
done

