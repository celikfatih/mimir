#!/bin/sh
set -e

# Generate read_only.xml from template if project group name is configured
if [ -n "$OPENGROK_PROJECT_GROUP_NAME" ]; then
    TEMPLATE_FILE="/opengrok/etc/read_only.xml.template"
    OUTPUT_FILE="/opengrok/etc/read_only.xml"

    if [ -f "$TEMPLATE_FILE" ]; then
        sed "s/{GROUP_NAME}/$OPENGROK_PROJECT_GROUP_NAME/g" "$TEMPLATE_FILE" > "$OUTPUT_FILE"
        echo "[entrypoint] Generated $OUTPUT_FILE with group: $OPENGROK_PROJECT_GROUP_NAME"
    else
        echo "[entrypoint] WARNING: Template file $TEMPLATE_FILE not found, skipping group configuration."
    fi
else
    echo "[entrypoint] OPENGROK_PROJECT_GROUP_NAME not set, skipping group configuration."
fi

# Execute the original OpenGrok entrypoint
exec python3 /scripts/start.py "$@"
