{{- define "swiftcart.name" -}}
{{- .Chart.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- define "swiftcart.fullname" -}}
{{- printf "%s-%s" .Release.Name (include "swiftcart.name" .) | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- define "swiftcart.labels" -}}
app.kubernetes.io/name: {{ include "swiftcart.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
helm.sh/chart: {{ printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" }}
{{- end -}}
{{- define "swiftcart.selectorLabels" -}}
app.kubernetes.io/name: {{ include "swiftcart.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end -}}
