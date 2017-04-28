cp ./summaryhuman.txt ./summaryhumannew.txt
while IFS= read -r line
do
	playid=`echo $line | cut -d',' -f1`
	playtile=`echo $line | cut -d',' -f2`
  echo $playid $playtile
  sed -i -r "s/^$playid/$playid\/$playtile/g" ./summaryhumannew.txt
done < ./aotm_playlist_titles.csv
