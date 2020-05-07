using UnityEngine;
using System.Collections;

public class h : MonoBehaviour {

	// Use this for initialization
	void Start () {
	
	}
	
	// Update is called once per frame
	void Update () {
        rigidbody2D.velocity = transform.right * 3;
	}
}
