<h1>Programmed on/off for EC2 instances</h1>

<h2>AWS Services Used</h2>
<ul>
  <li>AWS AutoScaling</li>
    <ol>
      <li>Modify the desired ability to turn off or turn on instances.</li>
    </ol>
  <li>AWS Lambda</li>
    <ol>
      <li>Executes the python code using a Eventbridge rule</li>
    </ol>
  <li>AWS Eventbridge</li>
    <ol>
      <li>Create a scheduled rule to execute the lambda function</li>
    </ol>
</ul> 
