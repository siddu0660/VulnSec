package main

import (
	"bufio"
	"encoding/base64"
	"encoding/xml"
	"errors"
	"fmt"
	"os"
	"os/exec"
	"strings"

	"github.com/Siddu0660/VulnSec/schema"
)

var username string = ""
var password string = ""

func getUserInput(msg string) string {
	fmt.Print(msg)
	reader := bufio.NewReader(os.Stdin)
	input, _ := reader.ReadString('\n')
	input = strings.TrimSpace(input)

	return input
}

func cmdWrapper() []string {
	wrapper := []string{"sudo", "-u", "_gvm", "gvm-cli", "--gmp-username", username, "--gmp-password", password, "socket", "--xml"}
	return wrapper
}

func authenticate() {
	reader := bufio.NewReader(os.Stdin)

	// Get gmp-username
	username = getUserInput("Enter your gmp username: ")

	// Get gmp-password
	fmt.Print("Enter the password for the user: ")
	password, _ = reader.ReadString('\n')
	password = password[:len(password) - 1]

	_, err := checkRun()

	if err != nil {
		fmt.Print("Invalid credentials.")
		username = ""
		password = ""
	}
}

func checkRun() (string, error) {
	cmd := cmdWrapper()
	cmd = append(cmd, "<get_version/>")

	out, err := exec.Command(cmd[0], cmd[1:]...).CombinedOutput()
	if err != nil {
		fmt.Println("Error getting version.", err)
		return "", err
	}

	return string(out), nil
}

func createTarget() (string, error) {
	// Get the target name
	targetName := getUserInput("Enter the name of the target to be created: ")
	
	// Maybe add asset hosts later
	// Get list of hosts to be scanned
	hostList := getUserInput("Enter a comma-separated list of hosts/host ranges (e.g., 192.168.0.1,192.168.0.0/24,192.168.0.5-192.168.0.10): ")
	
	// Maybe add port lists later
	// Get list of port ranges to be scanned
	portRanges := getUserInput("Enter a comma-separated list of port ranges (e.g., 20-80,100-200): ")
	
	xmlPayload := fmt.Sprintf(
		`<create_target><name>%s</name><hosts>%s</hosts><port_range>%s</port_range></create_target>`,
		targetName, hostList, portRanges,
	)
	
	cmd := cmdWrapper()
	cmd = append(cmd, xmlPayload)
	
	out, err := exec.Command(cmd[0], cmd[1:]...).CombinedOutput()
	print(string(out))
	if err != nil {
		fmt.Printf("Error creating target: %s\n", string(out))
		return "", err
	}
	var response schema.CreateTargetResponse
	err = xml.Unmarshal([]byte(out), &response)
	
	if err != nil {
		fmt.Print("Error parsing xml response.", err)
		return "", err
	}
	
	if response.Status != "201" {
		fmt.Printf("Error creating target: %s\n", response.StatusText)
		err = errors.New(response.StatusText)
		return "", err
	}
	
	fmt.Printf("Successfully created target.")
	return response.StatusText, nil
}

func createTask() (string, error) {
	// Get the task name
	taskName := getUserInput("Enter the name of the task: ")
	
	// Get available targets
	targets, err := getAllTargets()
	
	if err != nil {
		fmt.Print("Error getting targets: ", err)
		return "", err
	}
	
	fmt.Print("Enter the serial number of the target for the task.\n")
	for idx, target := range targets {
		fmt.Printf("%d. Name = %s, ID = %s, Hosts = %s\n", idx+1, target.Name, target.ID, target.Hosts)
	}
	var numTarget int
	_, err = fmt.Scan(&numTarget)

	if numTarget <= 0 || numTarget > len(targets) {
		fmt.Print("Invalid target selected.")
		err = errors.New("Target index out of bounds.")
		return "", err
	}

	configs, err := getAllConfigs()

	if err != nil {
		fmt.Print("Error getting configurations: ", err)
		return "", err
	}

	fmt.Print("Enter the serial number of the configuration to be used.\n")

	for idx, config := range configs {
		fmt.Printf("%d. Name = %s. Description: %s\n", idx+1, config.Name, config.Comment)
	}

	var numConfig int
	_, err = fmt.Scan(&numConfig)
	
	if numConfig <= 0 || numConfig > len(configs) {
		fmt.Print("Invalid config selected.")
		err = errors.New("Config index out of bounds.")
		return "", err
	}
	
	defaultScannerID := "08b69003-5fc2-4037-a479-93b440211c73"
	
	xmlPayload := fmt.Sprintf(`<create_task><name>%s</name><target id="%s"/><config id="%s"/><scanner id="%s"/></create_task>`, taskName, targets[numTarget - 1].ID, configs[numConfig - 1].ID, defaultScannerID)

	cmd := cmdWrapper()
	cmd = append(cmd, xmlPayload)

	out, err := exec.Command(cmd[0], cmd[1:]...).CombinedOutput()

	fmt.Print(string(out))
	if err != nil {
		fmt.Print("Error creating task: ", err)
		return "", err
	}
	
	return "", nil
}

func startTask() (string, error){
	fmt.Print("Enter the index of the task that you want to start.\n")

	tasks, err := getAllTasks()

	if err != nil {
		fmt.Print("Error getting existing tasks.")
		return "", err
	}

	for idx, task := range tasks {
		fmt.Printf("%d. %s\n", idx + 1, task.Name)
	}

	var numTask int
	fmt.Scan(&numTask)

	if numTask <= 0 || numTask > len(tasks) {
		fmt.Print("Invalid task selected.")
		err = errors.New("Task index out of bounds.")
		return "", err
	}

	numTask = numTask - 1

	cmd := cmdWrapper()
	xmlPayload := fmt.Sprintf(`<start_task task_id="%s"/>`, tasks[numTask].ID)
	cmd = append(cmd, xmlPayload)

	out, err := exec.Command(cmd[0], cmd[1:]...).CombinedOutput()

	if err != nil {
		fmt.Print("Error starting task.")
		return "", err
	}

	var response schema.StartTaskResponse
	err = xml.Unmarshal([]byte(out), &response)

	if response.Status != "200" {
		fmt.Print(response.StatusText)
		err = errors.New(response.StatusText)
		return "", err
	}

	return response.ReportID, nil
}

func getReportPDF() (string, error) {
	reports, err := getAllReports()

	if err != nil {
		fmt.Print("Error getting existing reports.")
		return "", err
	}

	fmt.Print("Enter index of the report you want.\n")
	for idx, report := range reports {
		fmt.Printf("%d. %s, %s, %s\n", idx + 1, report.Name, report.InnerReport.Task.Name, report.InnerReport.ScanRunStatus)
	}

	var numReport int
	fmt.Scan(&numReport)

	if numReport <= 0 || numReport > len(reports){
		fmt.Print("Invalid report selected.")
		err = errors.New("Invalid report index selected.")
		return "", err
	}

	pdfFormatID := "c402cc3e-b531-11e1-9163-406186ea4fc5"

	xmlPayload := fmt.Sprintf(`<get_reports report_id="%s" format_id = "%s" details="1" />`, reports[numReport-1].ID, pdfFormatID)
	cmd := cmdWrapper()
	cmd = append(cmd, xmlPayload)
	out, err := exec.Command(cmd[0], cmd[1:]...).CombinedOutput()
	
	if err != nil {
		fmt.Print("Failed to get report.")
		return "", err
	}
	
	var response schema.PDFReport
	err = xml.Unmarshal([]byte(out), &response)

	if err != nil {
		fmt.Print("Failed to get report text.", err)
		return "", err
	}

	pdfData, err := base64.StdEncoding.DecodeString(response.ReportText)

	if err != nil {
		fmt.Print("Failed to save the data as PDF.")
		return "", err
	}

	filename := fmt.Sprintf("report_%s.pdf", reports[numReport-1].Name)
	err = os.WriteFile(filename, pdfData, 0644)

	if err != nil {
		fmt.Printf("Failed to save as PDF.")
		return "", err
	}

	fmt.Printf("Report successfully saved to %s", filename)
	return "", nil
}

func getAllReports() ([]schema.Report, error) {
	cmd := cmdWrapper()
	xmlPayload := "<get_reports/>"
	cmd = append(cmd, xmlPayload)

	out, err := exec.Command(cmd[0], cmd[1:]...).CombinedOutput()

	if err != nil {
		fmt.Print("Error getting reports.")
		return nil, err
	}

	var response schema.GetReportsResponse
	err = xml.Unmarshal([]byte(out), &response)

	if err != nil {
		fmt.Print("Error extracting reports.")
		return nil, err
	}

	return response.Reports, nil
}

func getAllTargets() ([]schema.Target, error) {
	cmd := cmdWrapper()
	
	xmlPayload := `<get_targets/>`
	cmd = append(cmd, xmlPayload)
	
	out, err := exec.Command(cmd[0], cmd[1:]...).CombinedOutput()
	
	if err != nil {
		return nil, err
	}
	
	var response schema.GetTargetResponse
	err = xml.Unmarshal([]byte(out), &response)
	
	if response.Status != "200" {
		fmt.Print(response.StatusText)
		err = errors.New(response.StatusText)
		return nil, err
	}
	
	return response.Targets, nil
}

func getAllConfigs() ([]schema.Config, error) {
	cmd := cmdWrapper()
	xmlPayload := "<get_configs/>"
	cmd = append(cmd, xmlPayload)

	out, err := exec.Command(cmd[0], cmd[1:]...).CombinedOutput()

	if err != nil {
		fmt.Println(err)
		return nil, err
	}

	var response schema.GetConfigsResponse
	err = xml.Unmarshal([]byte(out), &response)

	if response.Status != "200" {
		fmt.Print(response.StatusText)
		err = errors.New(response.StatusText)
		return nil, err
	}
	
	return response.Configs, nil
}

func getAllTasks() ([]schema.Task, error) {
	cmd := cmdWrapper()
	xmlPayload := "<get_tasks/>"
	cmd = append(cmd, xmlPayload)

	out, err := exec.Command(cmd[0], cmd[1:]...).CombinedOutput()

	if err != nil {
		fmt.Println(err)
		return nil, err
	}

	var response schema.GetTasksResponse
	err = xml.Unmarshal([]byte(out), &response)

	if response.Status != "200" {
		fmt.Print(response.StatusText)
		err = errors.New(response.StatusText)
		return nil, err
	}

	return response.Tasks, nil
}


func main() {
	authenticate()
	
	fmt.Print("Choose what you want to do. (Enter a single number) \n")
	fmt.Print("1. Create a target to scan.\n")
	fmt.Print("2. Create a scan task.\n")
	fmt.Print("3. Start a scan task.\n")
	fmt.Print("4. Download a report for a scan.\n")

	var option int
	fmt.Scan(&option)

	switch option {
	case 1:
		createTarget()
	case 2:
		createTask()
	case 3:
		startTask()
	case 4:
		getReportPDF()
	default:
		fmt.Print("Invalid option selected.")
	}
}
