package sfa.mc.bajaj.gladminds.com.bajaj_mc_sfa;

import android.app.AlertDialog;
import android.app.ProgressDialog;
import android.content.ActivityNotFoundException;
import android.content.DialogInterface;
import android.content.Intent;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Environment;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;

import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.DefaultHttpClient;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.math.BigInteger;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class MainViewActivity extends AppCompatActivity {




    EditText useridEditText,passWordEditText;
    private ProgressDialog progressDialog;
    LinearLayout invalid_Log_in;
    TextView tv;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main_view);

        if(isNetworkAvailable()){
            // do network operation here
        }else{
            Toast.makeText(this, "Network Not Available . Please connect it now", Toast.LENGTH_SHORT).show();
            return;
        }



        useridEditText = (EditText) findViewById(R.id.etUserName);
        passWordEditText = (EditText) findViewById(R.id.etPass);
        invalid_Log_in=(LinearLayout)findViewById(R.id.ll_invalid);
        tv=(TextView) findViewById(R.id.tv_opn_time1);

        findViewById(R.id.btnSingIn).setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View arg0) {


                final String user_id = useridEditText.getText().toString();
                final String pass = passWordEditText.getText().toString();
/**

                if (!isValidEmail(user_id)) {
                    useridEditText.setError("Invalid Email");
                }

                if (!isValidPassword(pass)) {
                    passWordEditText.setError("Invalid Password");
                }
**/
                if (!user_id.equals("")&& !pass.equals("")) {

                    Intent myIntent = new Intent(getApplicationContext(),MenuView_Activity.class);
                    startActivity(myIntent);
                    overridePendingTransition(R.anim.push_down_in, R.anim.push_down_out);
                    myIntent.putExtra("email", useridEditText.getText().toString());
                    myIntent.putExtra("pass", passWordEditText.getText().toString());


              //new HttpAsyncTask().execute("http://192.168.0.50:8000/api-token-auth/");
                }
           }
        });

        findViewById(R.id.imv_ph_nm).setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View arg0) {


                onMakeCall();



            }
        });
        findViewById(R.id.imv_email).setOnClickListener(new View.OnClickListener(){

                @Override
                public void onClick(View arg0){

                    TextView tv_email = (TextView) findViewById(R.id.tv_email);
                    String email = tv_email.getText().toString();
                    onEmail_Send(email);
                }
         });
    }


    public  String POST(String url){
        InputStream inputStream = null;
        String result = "";
        try {

            // 1. create HttpClient
            HttpClient httpclient = new DefaultHttpClient();

            // 2. make POST request to the given URL
            HttpPost httpPost = new HttpPost(url);

            String json = "";


            // 3. build jsonObject


            JSONObject jsonObject = new JSONObject();
            jsonObject.accumulate("username", useridEditText.getText().toString());
            jsonObject.accumulate("password", passWordEditText.getText().toString());
            //jsonObject.accumulate("twitter", person.getTwitter());

            // 4. convert JSONObject to JSON to String
            json = jsonObject.toString();



            // 5. set json to StringEntity
            StringEntity se = new StringEntity(json);

            // 6. set httpPost Entity
            httpPost.setEntity(se);

            // 7. Set some headers to inform server about the type of the content
            httpPost.setHeader("Accept", "application/json");
            httpPost.setHeader("Content-type", "application/json");

            // 8. Execute POST request to the given URL
            HttpResponse httpResponse = httpclient.execute(httpPost);

            // 9. receive response as inputStream
            inputStream = httpResponse.getEntity().getContent();


            // 10. convert inputstream to string
            if(inputStream != null)
                result = convertInputStreamToString(inputStream);
            else
                result = "Did not work!";

        } catch (Exception e) {
            Log.d("InputStream", e.getLocalizedMessage());
        }

        // 11. return result
        return result;
    }

    private static String convertInputStreamToString(InputStream inputStream) throws IOException{
        BufferedReader bufferedReader = new BufferedReader( new InputStreamReader(inputStream));
        String line = "";
        String result = "";
        while((line = bufferedReader.readLine()) != null)
            result += line;

        inputStream.close();
        return result;

    }



    private class HttpAsyncTask extends AsyncTask<String, Void, String> {

        String param1=useridEditText.getText().toString();
        String param2=passWordEditText.getText().toString();
        @Override
        protected void onPreExecute()
        {
            //super.onPreExecute();
            //spinner.setVisibility(View.VISIBLE);


                }
        @Override
        protected String doInBackground(String... urls) {


            Log.d("User", param1);
            Log.d("pass", param2);

            return POST(urls[0]);
        }
        // onPostExecute displays the results of the AsyncTask.
        @Override
        protected void onPostExecute(String result) {

            Log.d("response-server1", result);
            tv.setText(result);



            try {

                    JSONObject jObj = new JSONObject(result);
                    String response = jObj.getString("token");
                    Log.d("response-server", response);

                    if(!response.equals("")){
                        Intent myIntent = new Intent(getApplicationContext(),Test.class);
                        myIntent.putExtra("email", useridEditText.getText().toString());
                        myIntent.putExtra("pass", passWordEditText.getText().toString());
                        startActivity(myIntent);
                    }


            } catch (JSONException e) {
                Log.e("MYAPP", "unexpected JSON exception", e);
                // Do something to recover ... or kill the app.
            }


        }
    }


    public boolean isNetworkAvailable() {
        ConnectivityManager connectivityManager = (ConnectivityManager) getApplicationContext().getSystemService(getApplicationContext().CONNECTIVITY_SERVICE);
        NetworkInfo activeNetworkInfo = connectivityManager.getActiveNetworkInfo();
        return activeNetworkInfo != null && activeNetworkInfo.isConnected();
    }

    // validating email id
    private boolean isValidEmail(String email) {
        String EMAIL_PATTERN = "^[_A-Za-z0-9-\\+]+(\\.[_A-Za-z0-9-]+)*@"
                + "[A-Za-z0-9-]+(\\.[A-Za-z0-9]+)*(\\.[A-Za-z]{2,})$";


        if(email.equals("")){
            useridEditText.setError("Insert UserID");
            return false;
            }

            Pattern pattern = Pattern.compile(EMAIL_PATTERN);
            Matcher matcher = pattern.matcher(email);
            return matcher.matches();


    }

    // validating password with retype password
    private boolean isValidPassword(String pass) {

        if(pass.equals("")){
            passWordEditText.setError("Insert Password");
            return false;

        }


        if (pass != null && pass.length() > 3) {
            if(pass.equals("1234"))
            return true;
        }
        return false;
    }

    //	<<	Alert Message for Phone>>
    public void onMakeCall( ) {
        final BigInteger ph=new BigInteger("9818690998");
        AlertDialog.Builder builder = new AlertDialog.Builder(MainViewActivity.this);
        builder.setMessage("Calling Number "+ ""+ph +
                "\n"+"Do you want to continue")
                .setCancelable(false)
                .setPositiveButton("Cancel", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int id) {
                        dialog.cancel();
                    }
                })
                .setNegativeButton("Continue", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int id) {
//	       			<<<	To make call, exit from the main application	>>>
                        try {
                            Intent callIntent = new Intent(Intent.ACTION_CALL);
                            callIntent.setData(Uri.parse("tel:" + ph));
                            startActivity(callIntent);
                        } catch (ActivityNotFoundException e) {
                            Toast toast = Toast.makeText(getApplicationContext(), e.toString(), Toast.LENGTH_SHORT);
                            toast.show();
                        }

                    }
                });
        AlertDialog alert = builder.create();
        alert.show();

    }


    public void onEmail_Send(String email ){


        String[] TO = {email};
        Intent emailIntent = new Intent(android.content.Intent.ACTION_SEND);
        emailIntent.setType("plain/text");
        emailIntent.putExtra(Intent.EXTRA_EMAIL, TO);
        emailIntent.putExtra(android.content.Intent.EXTRA_SUBJECT, " Feedback from "+ getResources().getString(R.string.app_name));
        emailIntent.putExtra(android.content.Intent.EXTRA_TEXT,"");
        startActivity(Intent.createChooser(emailIntent, "Email:"));

    }

}
