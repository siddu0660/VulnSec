package schema

import "encoding/xml"

type CreateTargetResponse struct {
	XMLName xml.Name `xml:"create_target_response"`
	Status string `xml:"status,attr"`
	StatusText string `xml:"status_text,attr"`
	ID string `xml:"id,attr"`
}

type Target struct {
	ID string `xml:"id,attr"`
	Name string `xml:"name"`
	Hosts string `xml:"hosts"`
}

type GetTargetResponse struct {
	XMLName xml.Name `xml:"get_targets_response"`
	Status string `xml:"status,attr"`
	StatusText string `xml:"status_text,attr"`
	Targets []Target `xml:"target"`
}

type Config struct {
	ID string `xml:"id,attr"`
	Name string `xml:"name"`
	Comment string `xml:"comment"`
}

type GetConfigsResponse struct {
	XMLName xml.Name `xml:"get_configs_response"`
	Status string `xml:"status,attr"`
	StatusText string `xml:"status_text,attr"`
	Configs []Config `xml:"config"`
}

type Task struct {
	ID string `xml:"id,attr"`
	Name string `xml:"name"`
}

type GetTasksResponse struct {
	XMLName xml.Name `xml:"get_tasks_response"`
	Status string `xml:"status,attr"`
	StatusText string `xml:"status_text,attr"`
	Tasks []Task `xml:"task"`
}

type StartTaskResponse struct {
	XMLName xml.Name `xml:"start_task_response"`
	Status string `xml:"status,attr"`
	StatusText string `xml:"status_text,attr"`
	ReportID string `xml:"report_id"`
}

type GetReportsResponse struct {
	XMLName xml.Name `xml:"get_reports_response"`
	Status string `xml:"status,attr"`
	StatusText string `xml:"status_text,attr"`
	Reports []Report `xml:"report"`
}

type Report struct {
	XMLName xml.Name `xml:"report"`
	ID string `xml:"id,attr"`
	Name string `xml:"name"`
	InnerReport InnerReport `xml:"report"`
}

type InnerReport struct {
	Task Task `xml:"task"`
	ScanRunStatus string `xml:"scan_run_status"`
}

type PDFReport struct {
	XMLName xml.Name `xml:"get_reports_response"`
	ID string `xml:"id,attr"`
	ReportText string `xml:"report"`
}

