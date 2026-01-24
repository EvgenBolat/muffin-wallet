{{/*
Full chart name
*/}}
{{- define "muffin-wallet.fullname" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "muffin-wallet.labels" -}}
app: muffin-wallet
chart: "{{ .Chart.Name }}-{{ .Chart.Version }}"
{{- end }}

{{/*
Selector labels
*/}}
{{- define "muffin-wallet.selectorLabels" -}}
app: muffin-wallet
{{- end }}
