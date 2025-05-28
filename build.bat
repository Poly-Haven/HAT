@echo off
rm index.json
blender --factory-startup --command extension build
blender --factory-startup --command extension server-generate --repo-dir=.

echo Now fix index.json, ensure URL is correct
echo Create the release on GH and test the archive URL