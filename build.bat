rm index.json
blender --factory-startup --command extension build
blender --factory-startup --command extension server-generate --repo-dir=.