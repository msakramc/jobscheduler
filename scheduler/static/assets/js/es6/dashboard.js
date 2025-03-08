const CSV_TABLE_SORT = 'csv_table_sort'




$(document).ready(function () {
    const dashboardApp = {
        data: [],
        selected_job_status: 'all',
        searchKey: '',
        limit: 50,
        page: 1,
        pagination: {},
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        job_status: {
            all: 0,
            completed: 0,
            running: 0,
            pending: 0,
            failed:0,
        },
        job_analytics :{
            avg_wait_time: 0,
            high: 0,
            medium: 0,
            low: 0,
        },
        init() {

            setInterval(() => {
                dashboardApp.getData();
            }, 1000);

            const socket = new WebSocket('ws://localhost:8000/ws/chat/');
            socket.onopen = function(e) {
                console.log('WebSocket connection established');
                // Send a message to request job data
                socket.send(JSON.stringify({
                    'status': 'all',
                    'page': 1
                }));
            };

            socket.onmessage = function(e) {
                const data = JSON.parse(e.data);
                console.log('Received data:', data);
            
                // Process the received job status and job list data
                const jobStatus = data.job_status;
                const jobs = data.results;
                // Update your UI here
            };

            socket.onclose = function(e) {
                console.log('WebSocket connection closed');
            };

            socket.onerror = function(e) {
                console.error('WebSocket error:', e);
            };
            
            $('#create-job-model .btn.btn-primary').click(function () {
                const jobData = {
                    name: $('#name').val(),
                    estimated_duration: $('#estimated_duration').val(),
                    priority: $('#priority').val(),
                    deadline: $('#deadline').val()
                };
                dashboardApp.createJob(jobData)
                $('#create-job-model').modal('hide')
                
            })


            dashboardApp.getData()
        },
        createJob(jobData) {
            $.ajax({
                type: "POST",
                url: "/api/v1/createjob/",
                headers: {
                    'X-CSRFToken': this.csrfmiddlewaretoken  // Retrieve CSRF token
                },
                data: JSON.stringify(jobData),
                contentType: 'application/json',
                dataType: 'json',
                success: (res) => {
                if(res.name){

                }
                },
                error: (err) => {
                }
            })

        },

        renderTable() {

            $('#status_all').html(this.job_status.all)
            $('#status_completed').html(this.job_status.completed)
            $('#status_running').html(this.job_status.running)
            $('#status_pending').html(this.job_status.pending)
            $('#status_failed').html(this.job_status.failed)
            $('#avg_wait_time').html(this.job_analytics.avg_wait_time)
            $('#priority_high').html(this.job_analytics.high)
            $('#priority_medium').html(this.job_analytics.medium)
            $('#priority_low').html(this.job_analytics.low)

            if (this.data.length > 0) {
                let html = ''
                this.data.forEach((element, index) => {
                    html += `<tr class="${index % 2 == 0 ? 'even' : 'odd'}">
                        <td>${element.name}</td>
                        <td>${element.estimated_duration}</td>
                        <td>${element.priority}</td>
                        <td>${element.deadline}</td>
                        <td>${element.start_time || ""}</td>
                        <td>${element.end_time || ""}</td>
                        <td>${element.user}</td>
                        <td>${element.status}</td>
                        <td>${element.created_datetime}</td>
                    </tr>`
                })
                $('#storebookingData').html(html);

            } else {
                $('#storebookingData').html('<tr><td colspan="9">No Data</td></tr>');
                $('#holder').html('')
            }
        },
        getData() {
            $.ajax({
                type: "GET",
                url: "/api/v1/getjobs/",
                data: {
                    status: this.selected_job_status,
                    date_start: this.start_date,
                    date_end: this.end_date,
                    limit: this.limit,
                    search: this.searchKey,
                    page: this.page,
                },
                success: (res) => {
                    this.data = res.results.results
                    this.pagination = res.pagination
                    this.job_status = res.results.job_status
                    this.job_analytics = res.results.job_analytics
                    this.renderTable()
                },
                error: (err) => {
                    this.data = []
                    this.country_count = res.country_count
                    this.renderTable()
                }
            })
        },
    }
    document.dashboardApp = dashboardApp;
    dashboardApp.init()


    $('#searchKey').keyup(function () {
        dashboardApp.searchKey = $(this).val()
        dashboardApp.page = 1
        dashboardApp.getData()
    });
    $('.countbox').click(function () {
        let status = $(this).data('status')
        if (status !== dashboardApp.selected_job_status) {
            $('.countbox').removeClass('border-active')
            $(this).addClass('border-active')
            dashboardApp.selected_job_status = status
            dashboardApp.page = 1
            dashboardApp.getData()
        }
    })
    
})