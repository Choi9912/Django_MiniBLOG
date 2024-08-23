
document.addEventListener('DOMContentLoaded', function() {
    var ctx = document.getElementById('engagementChart').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Views', 'Likes', 'Followers'],
            datasets: [{
                data: [
                    {{ total_views|safe }},
                    {{ total_likes|safe }},
                    {{ follower_count|safe }}
                ],
                backgroundColor: [
                    'rgba(75, 192, 192, 0.8)',
                    'rgba(255, 99, 132, 0.8)',
                    'rgba(54, 162, 235, 0.8)'
                ],
                borderColor: [
                    'rgba(75, 192, 192, 1)',
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom',
                },
                title: {
                    display: true,
                    text: 'Engagement Distribution'
                }
            }
        }
    });
});
