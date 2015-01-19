out="src/buildinfo.json"

rm $out

touch $out

echo "{" >> $out

echo "    \"buildDate\" : \"`date`\"," >> $out

echo "    \"buildNumber\" : \"$BUILD_NUMBER\"," >> $out

echo "    \"buildVersion\" : \"$VERSION\"," >> $out

echo "    \"gitRevision\" : \"`git rev-list --count HEAD`\"" >> $out

echo "}" >> $out


