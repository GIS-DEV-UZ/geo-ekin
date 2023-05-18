var map = null;
var geojsonFeature = null;
var userFeaturesList = [];

if (user_id != null) {
  fetch(`/get_polygons/${user_id}`)
    .then((res) => res.json())
    .then((res) => {
      res.polygon_cad_number.forEach((cadastral_number) => {
        fetch(
          `https://map.agro.uz/api/land_user/read_geom_all?prefix=${cadastral_number}`
        )
          .then((res) => res.json())
          .then((res) => {
            let property = res[0].features[0].properties;
            propObj = {
              full_name: property.full_name,
              viloyat: property.viloyat,
              tuman: property.tuman,
              total_farmland_areas: property.total_farmland_areas,
              cadastral_number: property.cadastral_number,
            };
            makeFeatureTable(propObj);
          });
      });
    });
}

$("#exampleModal").on("show.bs.modal", (event) => {
  if (!map) {
    map = L.map("map").setView([41.311081, 69.240562], 13);

    L.tileLayer("http://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}", {
      attribution:
        '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    }).addTo(map);
  }
  setTimeout(function () {
    window.dispatchEvent(new Event("resize"));
  }, 500);
});

$(".search_cadastr").click(function (e) {
  e.preventDefault();
  cadastral_number = $(".cad_number").val();
  fetch(
    `https://map.agro.uz/api/land_user/read_geom_all?prefix=${cadastral_number}`
  )
    .then((res) => res.json())
    .then((geojsonFeature) => {
      polygon = L.geoJSON(geojsonFeature).addTo(map);
      polygon.setStyle({ fillColor: "blue" });
      map.fitBounds(polygon.getBounds());
    });
});

$(".save-polygon").click(function (e) {
  const properties = geojsonFeature[0].features[0].properties;
  propObj = {
    full_name: properties.full_name,
    viloyat: properties.viloyat,
    tuman: properties.tuman,
    total_farmland_areas: properties.total_farmland_areas,
    cadastral_number: properties.cadastral_number,
  };

  makeFeatureTable(propObj);

  fetch(`/save_polygon/${properties.cadastral_number}`)
    .then((res) => res.json())
    .then((res) => {
      console.log(res);
    });
});

function makeFeatureTable(featureObj) {
  userFeaturesList.push(featureObj);
  const elFarmerTableTbody = document.querySelector(
    ".profile-farmer__table tbody"
  );
  if (elFarmerTableTbody != null) {
    elFarmerTableTbody.innerHTML = "";
    userFeaturesList.forEach((feature) => {
      elFarmerTableTbody.innerHTML += `<tr>
          <td>${feature.full_name}</td>
          <td>${feature.viloyat}</td>
          <td>${feature.tuman}</td>
          <td>${feature.total_farmland_areas} ga</td>
          <td>
            <a href="/user/polygon?cad_number=${feature.cadastral_number}">
              <img src="../static/images/eye.svg" alt="">
            </a>
          </td>
        </tr>`;
    });
  }
}
