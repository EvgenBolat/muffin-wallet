{{- define "currency.baseName" -}}
{{- .Values.app.name | default .Chart.Name | trunc 63 | trimSuffix "-" -}}
{{- end }}

{{- define "currency.fullName" -}}
{{- include "currency.baseName" . -}}
{{- end }}

{{- define "currency.labels" -}}
app.kubernetes.io/name: {{ include "currency.baseName" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/managed-by: Helm
{{- end }}

{{- define "currency.selector" -}}
app.kubernetes.io/name: {{ include "currency.baseName" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{- define "currency.serviceAccount" -}}
{{- if .Values.account.enabled -}}
{{ .Values.account.name }}
{{- else -}}
default
{{- end -}}
{{- end }}
