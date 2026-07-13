#!/usr/bin/env bash
API_URL="http://localhost:5000/api/timeline_post"
NUMBER=$((RANDOM % 1000))

RESPONSE=$(curl -fsS -X POST "$API_URL" \
  -d "name=test $NUMBER" \
  -d "email=test$NUMBER@example.com" \
  -d "content=Hello from curl...$NUMBER")

ID=$(python3 -c 'import json,sys; data=json.load(sys.stdin); print(data.get("id", ""))' <<<"$RESPONSE")

echo "Created timeline post with ID: $ID"
echo "Retrieving timeline post with ID: $ID"

GET_RESPONSE=$(curl -fsS "$API_URL")

if python3 -c 'import json,sys; data=json.load(sys.stdin); post_id=sys.argv[1]; posts=data.get("timeline_posts", []); ids=[str(p.get("id", "")) for p in posts]; sys.exit(0 if post_id in ids else 1)' "$ID" <<<"$GET_RESPONSE"; then
    echo "Success: Post $ID was found!"
    echo "Deleting timeline post with ID: $ID"
    curl -fsS -X DELETE "$API_URL/$ID"
    echo "Deleted timeline post with ID: $ID"
else
    echo "Failure: Post $ID could not be verified."
    exit 1
fi
